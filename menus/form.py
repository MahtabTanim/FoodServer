from .models import Category
from django.forms import ModelForm
from django import forms


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "description"]
