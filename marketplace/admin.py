from django.contrib import admin

from marketplace.models import Cart, Tax


# Register your models here.
class CartManager(admin.ModelAdmin):
    list_display = ["user", "fooditem", "quantity", "pk"]


class TaxManager(admin.ModelAdmin):
    list_display = ["tax_type", "tax_percentage", "is_active"]
    list_editable = [
        "is_active",
    ]


admin.site.register(Cart, CartManager)
admin.site.register(Tax, TaxManager)
