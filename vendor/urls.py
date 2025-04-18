from django.urls import path
from . import views

from account.views import restaurantDashboard

urlpatterns = [
    path("", restaurantDashboard, name="vendor"),
    path("profile/", views.vprofile, name="vprofile"),
    path("menu-builder/", views.menu_builder, name="menu_builder"),
    path(
        "menu-builder/category/<int:pk>/",
        views.fooditmes_by_category,
        name="fooditmes_by_category",
    ),
    # category CRUD
    path("menu-builder/category/add", views.add_category, name="add_category"),
    path(
        "menu-builder/category/edit/<int:pk>", views.edit_category, name="edit_category"
    ),
    path(
        "menu-builder/category/delete/<int:pk>",
        views.delete_category,
        name="delete_category",
    ),
    # FoodITem Crud
    path("menu-builder/food/add", views.add_food, name="add_food"),
    path("menu-builder/food/edit/<int:pk>", views.edit_food, name="edit_food"),
    path(
        "menu-builder/food/delete/<int:pk>",
        views.delete_food,
        name="delete_food",
    ),
    # opening hours
    path("opening_hours", views.opening_hours, name="opening_hours"),
    path("opening_hours/add", views.add_opening_hours, name="add_opening_hours"),
    path(
        "opening_hours/remove/<int:pk>",
        views.remove_opening_hour,
        name="remove_opening_hour",
    ),
    # change password
    path("change_password/", views.change_password, name="change_password_vendor"),
    # all orders
    path("orders/", views.all_orders, name="all_orders"),
    path("orders/<str:order_number>", views.v_order_details, name="v_order_details"),
]
