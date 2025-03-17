from django.urls import include, path
from account.views import custDashboard
from . import views

urlpatterns = [
    path("", custDashboard, name="customer"),
    path("profile/", views.cprofile, name="cprofile"),
    path("myorders/", views.myorders, name="myorders"),
    path("myorders/<str:order_number>", views.order_details, name="order_details"),
    path("change_password", views.change_password, name="change_password"),
]
