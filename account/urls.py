from django.urls import path
from . import views

urlpatterns = [
    path("registerUser/", views.registerUser, name="registerUser"),
    path("registerVendor/", views.registerVendor, name="registerVendor"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("myAccount/", views.myAccount, name="myAccount"),
    path("custDashboard/", views.custDashboard, name="custDashboard"),
    path("restaurantDashboard/", views.restaurantDashboard, name="restaurantDashboard"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("forgotpassword/", views.forgotpassword, name="forgotpassword"),
    path(
        "resetpassword_validate/<uidb64>/<token>/",
        views.resetpassword_validate,
        name="resetpassword_validate",
    ),
    path("resetpassword/", views.resetpassword, name="resetpassword"),
]
