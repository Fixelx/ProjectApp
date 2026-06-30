#!/bin/bash
set -e

# ── Farben ──────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()     { echo -e "${GREEN}[✓]${NC} $1"; }
warn()    { echo -e "${YELLOW}[!]${NC} $1"; }
error()   { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# ── Konfiguration ────────────────────────────────────────
APP_DIR="/opt/projects"
REPO_URL="https://github.com/Fixelx/ProjectApp.git"
DOMAIN=${1:-"localhost"}

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   ProjectApp Deployment"
echo "   Domain: $DOMAIN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── Root check ───────────────────────────────────────────
[ "$EUID" -ne 0 ] && error "Bitte als root ausführen (sudo ./deploy.sh)"

# ── Locale fix ───────────────────────────────────────────
log "Locale einrichten..."
apt install -y locales -q
locale-gen en_US.UTF-8 de_DE.UTF-8
update-locale LANG=de_DE.UTF-8 LC_ALL=de_DE.UTF-8
export LC_ALL=de_DE.UTF-8
export LANG=de_DE.UTF-8

# ── System-Pakete ────────────────────────────────────────
log "System-Pakete installieren..."
apt update -q
apt install -y git nginx curl -q
apt install -y \
  libgobject-2.0-0 \
  libpango-1.0-0 \
  libpangoft2-1.0-0 \
  libpangocairo-1.0-0 \
  libcairo2 \
  libcairo-gobject2 \
  libgdk-pixbuf-2.0-0 \
  libffi-dev \
  shared-mime-info \
  fonts-liberation

# ── Python Version erkennen und richtige Pakete installieren ──
log "Python einrichten..."
PYTHON_BIN=""

# Python 3.13 vorhanden?
if python3 --version 2>/dev/null | grep -q "3.13"; then
    log "Python 3.13 erkannt"
    apt install -y python3.13-venv python3-pip -q || true
    # pip über get-pip.py nur wenn nicht vorhanden
    if ! python3 -m pip --version &>/dev/null; then
        curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
        python3 /tmp/get-pip.py --break-system-packages -q
    fi
    PYTHON_BIN="python3"
# Python 3.11 vorhanden?
elif python3.11 --version 2>/dev/null; then
    log "Python 3.11 erkannt"
    apt install -y python3.11 python3.11-venv python3-pip -q
    PYTHON_BIN="python3.11"
# Fallback: Python 3 installieren
else
    log "Python 3.11 installieren..."
    apt install -y python3 python3-venv python3-pip -q
    PYTHON_BIN="python3"
fi

log "Python-Binary: $PYTHON_BIN ($($PYTHON_BIN --version))"

# ── Repo ─────────────────────────────────────────────────
if [ -d "$APP_DIR/.git" ]; then
    log "Repo aktualisieren..."
    cd $APP_DIR
    git pull origin main
else
    log "Repo klonen..."
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR
fi

cd $APP_DIR

# ── .env prüfen ──────────────────────────────────────────
if [ ! -f "$APP_DIR/.env" ]; then
    warn ".env fehlt – wird aus .env.example erstellt..."
    cp $APP_DIR/.env.example $APP_DIR/.env

    SECRET=$($PYTHON_BIN -c "import secrets; print(secrets.token_urlsafe(50))")
    sed -i "s/^SECRET_KEY=.*/SECRET_KEY=$SECRET/" $APP_DIR/.env
    sed -i "s/^ALLOWED_HOSTS=.*/ALLOWED_HOSTS=$DOMAIN,localhost/" $APP_DIR/.env
    sed -i "s/^CSRF_TRUSTED_ORIGINS=.*/CSRF_TRUSTED_ORIGINS=https:\/\/$DOMAIN/" $APP_DIR/.env

    warn ".env wurde angelegt – bitte prüfen: nano $APP_DIR/.env"
fi

# ── Python venv ──────────────────────────────────────────
log "Virtualenv einrichten..."
$PYTHON_BIN -m venv $APP_DIR/venv
source $APP_DIR/venv/bin/activate

# ── Abhängigkeiten ───────────────────────────────────────
log "Python-Pakete installieren..."
pip install --upgrade pip -q
pip install -r $APP_DIR/requirements.txt -q
pip install gunicorn -q

# ── Django setup ─────────────────────────────────────────
log "Migrationen ausführen..."
python manage.py migrate --no-input

log "Static files sammeln..."
python manage.py collectstatic --no-input

# ── Gunicorn Service ─────────────────────────────────────
log "Gunicorn Service einrichten..."
cat > /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=Gunicorn für ProjectApp
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/gunicorn \\
    --workers 3 \\
    --bind unix:$APP_DIR/gunicorn.sock \\
    config.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable gunicorn -q
systemctl restart gunicorn

# ── Nginx config ─────────────────────────────────────────
log "Nginx konfigurieren..."
cat > /etc/nginx/sites-available/projectapp << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location /static/ {
        alias $APP_DIR/staticfiles/;
    }

    location /media/ {
        alias $APP_DIR/media/;
    }

    location / {
        proxy_pass http://unix:$APP_DIR/gunicorn.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

[ -f /etc/nginx/sites-enabled/default ] && rm /etc/nginx/sites-enabled/default

ln -sf /etc/nginx/sites-available/projectapp /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx

# ── Superuser ────────────────────────────────────────────
warn "Superuser anlegen? [j/N]"
read -r SU
if [ "$SU" = "j" ] || [ "$SU" = "J" ]; then
    python manage.py createsuperuser
fi

# ── Fertig ───────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "Deployment abgeschlossen!"
echo ""
echo "  App erreichbar unter: http://$DOMAIN"
echo "  .env prüfen:          nano $APP_DIR/.env"
echo "  Logs:                 journalctl -u gunicorn -f"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
