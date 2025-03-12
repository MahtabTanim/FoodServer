from django.urls import include, path
from account.views import custDashboard
from . import views

urlpatterns = [
    path("", custDashboard, name="customer"),
    path("profile/", views.cprofile, name="cprofile"),
]
