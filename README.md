Installation
bash <(curl -s https://raw.githubusercontent.com/Fixelx/ProjectApp/main/deploy.sh) meine-domain.de

Auto: Felix Baumann

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
