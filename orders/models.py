from django.db import models
from account.models import User
from menus.models import FoodItem
from vendor.models import Vendor

# Create your models here.
request_object = ""


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(default="ssl", max_length=100)
    amount = models.CharField(max_length=12)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(models.Model):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    vendors = models.ManyToManyField(Vendor, blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, default="00000000000")
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    total = models.FloatField()
    tax_data = models.JSONField(
        blank=True,
        help_text="Data format: {'tax_type':{'tax_percentage':'tax_amount'}}",
    )
    total_data = models.JSONField(blank=True, null=True)
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=15, choices=STATUS, default="New")
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.order_number

    @property
    def ordered_to(self):
        return ",".join([str(i) for i in self.vendors.all()])

    @property
    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user)
        total_data = self.total_data
        tax_data = total_data[str(vendor.id)]
        print(tax_data)
        t_data = {}
        for key, val in tax_data.items():
            subtotal = key
            t_data = val
        tax_data = t_data
        total_tax = 0
        for tax, data in tax_data.items():
            for key, val in data.items():
                total_tax += round(float(subtotal) * float(key) / 100, 2)
        return {
            str(total_tax + round(float(subtotal), 2)): {
                str(round(float(subtotal), 2)): str(total_tax)
            }
        }


class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fooditem.food_title
