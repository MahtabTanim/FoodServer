from django.urls import path
from . import views

from account.views import restaurantDashboard

urlpatterns = [
    path("", restaurantDashboard, name="vendor"),
    path("profile/", views.vprofile, name="vprofile"),
]
