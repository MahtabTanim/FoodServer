from django.contrib import admin
from .models import Payment, OrderedFood, Order


# Register your models here.
class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = [
        "order",
        "payment",
        "user",
        "fooditem",
        "quantity",
        "price",
        "amount",
    ]
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number",
        "name",
        "phone",
        "email",
        "total",
        "payment_method",
        "status",
        "is_ordered",
        "ordered_to",
        "created_at",
    ]
    inlines = [
        OrderedFoodInline,
    ]


admin.site.register(Payment)
admin.site.register(OrderedFood)
admin.site.register(Order, OrderAdmin)
