from django.contrib import admin
from .models import Payment, OrderedFood, Order

# Register your models here.

admin.site.register(Payment)
admin.site.register(OrderedFood)
admin.site.register(Order)
