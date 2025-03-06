from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from marketplace.context_processors import get_cart_counter, get_cart_total
from menus.models import Category, FoodItem
from .models import Cart
from vendor.models import Vendor
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    context = {
        "vendor_count": len(vendors),
        "vendors": vendors,
    }
    return render(request, "marketplace/listings.html", context)


def vendor_detail(request, vendor_slug):
    vendor = Vendor.objects.get(vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            "fooditems",
            queryset=FoodItem.objects.filter(is_available=True),
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        "vendor": vendor,
        "categories": categories,
        "cart_items": cart_items,
    }
    return render(request, "marketplace/vendor_detail.html", context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        # checking AJAX request
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":

            try:
                # Checking Food Item
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    # Checking Cart
                    fcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # print("cart found with this food , incresing quantity")
                    fcart.quantity += 1
                    fcart.save()
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": "Increased cart quantity ",
                            "cart_counter": get_cart_counter(request),
                            "qty": fcart.quantity,
                            "get_cart_total": get_cart_total(request),
                        }
                    )
                except:
                    # print("cart not found , creating new")
                    fcart = Cart.objects.create(
                        fooditem=fooditem, user=request.user, quantity=1
                    )
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": "Created new cart ",
                            "cart_counter": get_cart_counter(request),
                            "qty": 1,
                            "get_cart_total": get_cart_total(request),
                        }
                    )

            except:
                return JsonResponse(
                    {"status": "failed", "message": "fooditem doesn't exists"}
                )
        else:
            return JsonResponse({"status": "failed", "message": "not ajax request"})
    else:
        return JsonResponse(
            {"status": "login_required", "message": "Please login to continue"}
        )


def remove_from_cart(request, food_id):
    if request.user.is_authenticated:
        # checking AJAX request
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":

            try:
                # Checking Food Item
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    # Checking Cart
                    fcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # print("cart found with this food , decresing quantity")
                    qty = 0
                    if fcart.quantity > 1:
                        fcart.quantity -= 1
                        fcart.save()
                        qty = fcart.quantity
                    else:
                        fcart.delete()
                        qty = 0
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": "Decreased cart quantity ",
                            "cart_counter": get_cart_counter(request),
                            "qty": qty,
                            "get_cart_total": get_cart_total(request),
                        }
                    )
                except:
                    # print("cart not found , doing nothing new")
                    return JsonResponse(
                        {
                            "status": "failed",
                            "message": "You do not have this item in your cart",
                            "cart_counter": get_cart_counter(request),
                            "qty": 0,
                            "get_cart_total": get_cart_total(request),
                        }
                    )

            except:
                return JsonResponse(
                    {"status": "failed", "message": "fooditem doesn't exists"}
                )
        else:
            return JsonResponse({"status": "failed", "message": "not ajax request"})
    else:
        return JsonResponse(
            {"status": "login_required", "message": "Please login to continue"}
        )


@login_required(login_url="login")
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by("-updated_at")
    context = {
        "cart_items": cart_items,
    }
    return render(request, "marketplace/cart.html", context)


@login_required(login_url="login")
def delete_cart_item(request, cart_id):
    if request.user.is_authenticated:
        # checking AJAX request
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            try:
                cart_item = Cart.objects.filter(user=request.user, id=cart_id)
                cart_item.delete()
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Cart item deleted successfully",
                        "cart_counter": get_cart_counter(request),
                        "get_cart_total": get_cart_total(request),
                    }
                )
            except:
                return JsonResponse(
                    {"status": "failed", "message": "cart item doesn't exists"}
                )
        else:
            return JsonResponse({"status": "failed", "message": "not ajax request"})
    else:
        return JsonResponse(
            {"status": "login_required", "message": "Please login to continue"}
        )


def search(request):
    address = request.GET.get("address")
    restaurant_name = request.GET.get("restaurant_name")
    latitude = request.GET.get("latitude")
    longitude = request.GET.get("longitude")
    radius = request.GET.get("radius")
    fetch_vendors_by_fooditems = FoodItem.objects.filter(
        food_title__icontains=restaurant_name, is_available=True
    ).values_list("vendor", flat=True)
    vendors = Vendor.objects.filter(
        Q(id__in=fetch_vendors_by_fooditems)
        | Q(
            is_approved=True,
            user__is_active=True,
            vendor_name__icontains=restaurant_name,
        )
    )
    context = {
        "vendor_count": len(vendors),
        "vendors": vendors,
    }
    return render(request, "marketplace/listings.html", context)
