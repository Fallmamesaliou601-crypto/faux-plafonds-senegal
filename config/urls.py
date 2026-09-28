from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from core.views import home
from core.admin_dashboard import dashboard


urlpatterns = [
    path("admin/tableau-de-bord/", dashboard, name="tableau_de_bord"),
    path("admin/", admin.site.urls),
    path("", home, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
