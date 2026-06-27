from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("projects/", include("projects.urls")),
    path("projects/", include("finance.urls")),
    path("projects/", include("documents.urls")),
    path("projects/", include("time_tracking.urls")),
    path("projects/", include("inventory.urls")),
    path("inventory/", include("inventory.urls_global")),
    path("invoices/", include("invoices.urls")),
    path("settings/", include("masterdata.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls")),]