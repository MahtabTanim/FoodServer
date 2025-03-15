from datetime import date, datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render

from account.models import UserProfile
from marketplace.context_processors import get_cart_counter, get_cart_total
from marketplace.forms import OrderForm
from menus.models import Category, FoodItem
from .models import Cart
from vendor.models import Vendor
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from vendor.models import OpeningHour
from vendor.views import get_vendor

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
    current_openings = None
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        hours = OpeningHour.objects.filter(vendor=vendor).order_by("day", "from_hour")
        current_openings = OpeningHour.objects.filter(
            vendor=vendor, day=date.today().isoweekday()
        )

    else:
        cart_items = None
        hours = None
    context = {
        "vendor": vendor,
        "categories": categories,
        "cart_items": cart_items,
        "opening_hours": hours,
        "current_openings": current_openings,
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
    if not address:
        return redirect("marketplace")
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
    if latitude and longitude and radius:
        pnt = GEOSGeometry(f"POINT({longitude} {latitude})", srid=4326)
        vendors = (
            Vendor.objects.filter(
                Q(id__in=fetch_vendors_by_fooditems)
                | Q(
                    is_approved=True,
                    user__is_active=True,
                    vendor_name__icontains=restaurant_name,
                ),
                user_profile__location__distance_lte=(pnt, D(km=radius)),
            )
            .annotate(distance=Distance("user_profile__location", pnt))
            .order_by("distance")
        )
        for v in vendors:
            v.kms = round(v.distance.km, 1)
    context = {
        "vendor_count": len(vendors),
        "vendors": vendors,
        "source_location": address,
    }
    return render(request, "marketplace/listings.html", context)


@login_required(login_url="login")
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by("-updated_at")
    if cart_items.count() <= 0:
        return redirect("marketplace")
    user_profile = UserProfile.objects.get(user=request.user)
    initial_values = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "phone": request.user.phone_number,
        "email": request.user.email,
        "address": user_profile.address,
        "country": user_profile.country,
        "state": user_profile.state,
        "city": user_profile.city,
        "pin_code": user_profile.pin_code,
    }
    form = OrderForm(initial=initial_values)
    context = {"cart_items": cart_items, "form": form}
    return render(request, "marketplace/checkout.html", context)
