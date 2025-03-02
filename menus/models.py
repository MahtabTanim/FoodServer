from django.db import models
from vendor.models import Vendor

# Create your models here.


class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(unique=True, max_length=60)
    slug = models.SlugField(max_length=60, unique=True)
    description = models.TextField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name

    def clean(self):
        self.category_name = self.category_name.capitalize()


class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    food_title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to="foodItemImages")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    description = models.TextField(max_length=300, blank=True, default="Food ")

    def __str__(self):
        return self.food_title
