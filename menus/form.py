from .models import Category, FoodItem
from django import forms
from account.validators import allow_only_image_validator


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "description"]


class FoodItemForm(forms.ModelForm):
    image = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info w-100"}),
        validators=[allow_only_image_validator],
    )

    class Meta:

        model = FoodItem
        fields = [
            "category",
            "food_title",
            "price",
            "image",
            "description",
            "is_available",
        ]

    def __init__(self, *args, **kwargs):
        vendor = kwargs.pop("vendor", None)
        super(FoodItemForm, self).__init__(*args, **kwargs)
        if vendor:
            self.fields["category"].queryset = Category.objects.filter(vendor=vendor)
