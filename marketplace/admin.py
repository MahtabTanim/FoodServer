from django.contrib import admin

from marketplace.models import Cart


# Register your models here.
class CartManager(admin.ModelAdmin):
    list_display = ["user", "fooditem", "quantity", "pk"]


admin.site.register(Cart, CartManager)
