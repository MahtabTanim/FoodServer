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
from menus.form import CategoryForm, FoodItemForm
from django.contrib import messages
from django.template.defaultfilters import slugify
from .forms import OpeningHourForm
from .models import OpeningHour
from django.http import JsonResponse
from django.db import IntegrityError


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
            vendor = vendor_form.save(commit=False)
            vendor_name = vendor_form.cleaned_data["vendor_name"]
            slug = slugify(vendor_name) + "-" + str(vendor.user.id)
            vendor.vendor_slug = slug
            vendor.save()
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
        form = CategoryForm()
    context = {
        "categoryForm": form,
    }
    return render(request, "vendor/add_category.html", context)


@login_required(login_url="login")
@user_passes_test(check_restaurant)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk, vendor=get_vendor(request))
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
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


@login_required(login_url="login")
@user_passes_test(check_restaurant)
def add_food(request):
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.cleaned_data["category"]
            food_title = form.cleaned_data["food_title"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            description = form.cleaned_data["description"]
            is_available = form.cleaned_data["is_available"]
            vendor = get_vendor(request)
            slug = slugify(food_title)
            FoodItem.objects.create(
                vendor=vendor,
                category=category,
                food_title=food_title,
                slug=slug,
                price=price,
                image=image,
                description=description,
                is_available=is_available,
            )
            messages.success(request, "Food Item has been created Successfully")
            return redirect("fooditmes_by_category", category.id)

    else:
        form = FoodItemForm()
        form.fields["category"].queryset = Category.objects.filter(
            vendor=get_vendor(request)
        )
    context = {
        "foodItemForm": form,
    }
    return render(request, "vendor/add_food.html", context)


@login_required(login_url="login")
@user_passes_test(check_restaurant)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == "POST":
        print(request.POST)
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            foodTitle = form.cleaned_data["food_title"]
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodTitle)
            food.save()
            form.save()
            return redirect("fooditmes_by_category", form.cleaned_data["category"].id)
        else:
            messages.error(request, "Invalid Information")
            print(form.errors)
    form = FoodItemForm(
        instance=food,
    )
    form.fields["category"].queryset = Category.objects.filter(
        vendor=get_vendor(request)
    )
    context = {
        "food": food,
        "foodItemForm": form,
    }
    return render(request, "vendor/edit_food.html", context)


@login_required(login_url="login")
@user_passes_test(check_restaurant)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if food:
        food.delete()
        messages.info(request, "Food Item Deleted ")

    return redirect("fooditmes_by_category", food.category.id)


def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm()
    context = {
        "opening_hours": opening_hours,
        "form": form,
    }
    return render(request, "vendor/opening_hours.html", context)


def add_opening_hours(request):
    if request.user.is_authenticated:
        if (
            request.headers.get("X-Requested-With") == "XMLHttpRequest"
            and request.method == "POST"
        ):
            day = request.POST["day"]
            from_hour = request.POST["from_hour"]
            to_hour = request.POST["to_hour"]
            is_closed = request.POST["is_closed"]
            if is_closed == "false":
                is_closed = False
            else:
                is_closed = True
            try:
                hour = OpeningHour.objects.create(
                    vendor=get_vendor(request),
                    day=day,
                    from_hour=from_hour,
                    to_hour=to_hour,
                    is_closed=is_closed,
                )
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {
                            "status": "success",
                            "id": hour.id,
                            "day": day.get_day_display(),
                            "is_closed": "true",
                        }
                    else:
                        response = {
                            "status": "success",
                            "id": hour.id,
                            "day": day.get_day_display(),
                            "from_hour": hour.from_hour,
                            "to_hour": hour.to_hour,
                            "is_closed": "false",
                        }
                    return JsonResponse(response)
            except IntegrityError as e:
                return JsonResponse(
                    {
                        "status": "failed",
                        "message": str(e),
                    }
                )
        else:
            return JsonResponse(
                {
                    "status": "failed",
                    "message": "Not POST/AJAX request",
                }
            )
    else:
        return JsonResponse(
            {
                "status": "failed",
                "message": "Not authenticated",
            }
        )
