from django.urls import path
from . import views

urlpatterns = [
    path("place-order", views.place_order, name="place_order"),
    path("order/<str:order_id>", views.order, name="order"),
    path("status", views.status, name="status"),
    path(
        "complete/<str:val_id>/<str:tran_id>", views.ssl_complete, name="ssl_complete"
    ),
]
