from django.db import models

from account.models import User
from menus.models import FoodItem

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fooditem.food_title


class Tax(models.Model):
    tax_type = models.CharField(max_length=20, unique=True)
    tax_percentage = models.DecimalField(
        decimal_places=2, max_digits=4, verbose_name="Tax percentage (%)", default=0
    )
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Tax"

    def __str__(self):
        return self.tax_type
