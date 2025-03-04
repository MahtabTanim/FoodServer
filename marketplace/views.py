from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from menus.models import Category, FoodItem
from .models import Cart
from vendor.models import Vendor
from django.db.models import Prefetch

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
    context = {
        "vendor": vendor,
        "categories": categories,
    }
    return render(request, "marketplace/vendor_detail.html", context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    fcart = Cart.objects.get(fooditem=fooditem, user=request.user)
                    fcart.quantity += 1
                    fcart.save()
                    return JsonResponse(
                        {"status": "Success", "message": "Increased cart quantity "}
                    )
                except:
                    fcart = Cart.objects.create(
                        fooditem=fooditem, user=request.user, quantity=1
                    )
                    return JsonResponse(
                        {"status": "Success", "message": "Created new cart "}
                    )

            except:
                return JsonResponse(
                    {"status": "failed", "message": "fooditem doesn't exists"}
                )
        else:
            return JsonResponse({"status": "failed", "message": "not ajax request"})
    else:
        return JsonResponse(
            {"status": "failed", "message": "user is not  authenticated"}
        )
