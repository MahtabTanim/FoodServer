from django.http import HttpResponse
from django.shortcuts import render
from account.forms import UserProfileForm, VendorForm
from django.shortcuts import get_object_or_404, redirect
from .models import Vendor
from account.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from account.views import check_restaurant
from menus.models import Category
from menus.models import FoodItem
from menus.form import CategoryForm
from django.contrib import messages
from django.template.defaultfilters import slugify


def get_vendor(request):
    return Vendor.objects.get(user=request.user)


# Create your views here.
@login_required(login_url="login")
@user_passes_test(check_restaurant)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Profile Updated")
            return redirect("vprofile")
        else:
            context = {
                "profile_form": profile_form,
                "vendor_form": vendor_form,
            }
            return render(request, "vendor/vprofile.html", context)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
        context = {
            "profile_form": profile_form,
            "vendor_form": vendor_form,
        }
        return render(request, "vendor/vprofile.html", context)


@login_required(login_url="login")
@user_passes_test(check_restaurant)
def menu_builder(request):
    categories = Category.objects.filter(vendor=get_vendor(request)).order_by(
        "created_at"
    )
    context = {
        "categories": categories,
    }

    return render(request, "vendor/menu_builder.html", context)


@login_required(login_url="login")
@user_passes_test(check_restaurant)
def fooditmes_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    print(fooditems)
    context = {
        "fooditems": fooditems,
        "category": category,
    }

    return render(request, "vendor/fooditmes_by_category.html", context)


@login_required(login_url="login")
@user_passes_test(check_restaurant)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            description = form.cleaned_data["description"]
            vendor = get_vendor(request)
            slug = slugify(category_name)
            Category.objects.create(
                category_name=category_name,
                description=description,
                vendor=vendor,
                slug=slug,
            )
            messages.success(request, "Category has been created Successfully")
            return redirect("menu_builder")
        else:
            print(form.errors)
            # return render(request, "vendor/add_category.html", {"categoryForm": form})
    else:
        form = CategoryForm()
    context = {
        "categoryForm": form,
    }
    return render(request, "vendor/add_category.html", context)


@login_required(login_url="login")
@user_passes_test(check_restaurant)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully")
            return redirect("menu_builder")
        else:
            messages.error(request, "Invalid Information")
            print(form.errors)
    form = CategoryForm(instance=category)
    context = {
        "categoryForm": form,
        "category": category,
    }
    return render(request, "vendor/edit_category.html", context)


@login_required(login_url="login")
@user_passes_test(check_restaurant)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if category:
        category.delete()
        messages.info(request, "Category Deleted ")

    return redirect("menu_builder")
