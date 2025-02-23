from django.contrib import admin
from .models import Category, FoodItem
from django.contrib.admin import ModelAdmin


# Register your models here.
class CategoryManager(ModelAdmin):
    list_display = (
        "category_name",
        "description",
        "vendor",
    )
    prepopulated_fields = {"slug": ("category_name",)}
    list_display_links = [
        "vendor",
    ]
    search_fields = ["category_name", "vendor__vendor_name"]
    list_filter = ["category_name", "vendor__vendor_name"]


class FoodItemAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("food_title",)}
    list_display = ["food_title", "category", "vendor", "price", "is_available"]
    list_display_links = ["category", "vendor"]
    list_editable = ["is_available", "price"]
    search_fields = [
        "food_title",
        "vendor__vendor_name",
        "category__category_name",
        "price",
    ]
    list_filter = ["is_available", "category"]


admin.site.register(Category, CategoryManager)
admin.site.register(FoodItem, FoodItemAdmin)
