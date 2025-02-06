from django.conf import settings
from django.conf.urls.static import static

from .views import home
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("accounts/", include("account.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
