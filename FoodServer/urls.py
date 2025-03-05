from django.conf import settings
from django.conf.urls.static import static

from .views import home
from django.contrib import admin
from django.urls import path, include
from marketplace.views import cart

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("", include("account.urls")),
    path("marketplace/", include("marketplace.urls")),
    # cart
    path("cart/", cart, name="cart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
