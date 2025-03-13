from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from marketplace.forms import OrderForm
from marketplace.models import Cart
from marketplace.context_processors import get_cart_total
from orders.utils import generate_order_number
from .models import Order
from django.contrib import messages


# Create your views here.
@login_required(login_url="login")
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by("-updated_at")
    if cart_items.count() <= 0:
        return redirect("marketplace")

    subtotal = get_cart_total(request)["subtotal"]
    tax = get_cart_total(request)["tax"]
    total = get_cart_total(request)["total"]
    tax_data = get_cart_total(request)["tax_dict"]

    print(subtotal, tax, total, tax_data)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.user = request.user
            order.first_name = form.cleaned_data["first_name"]
            order.last_name = form.cleaned_data["last_name"]
            order.phone = form.cleaned_data["phone"]
            order.email = form.cleaned_data["email"]
            order.address = form.cleaned_data["address"]
            order.country = form.cleaned_data["country"]
            order.state = form.cleaned_data["state"]
            order.city = form.cleaned_data["city"]
            order.pin_code = form.cleaned_data["pin_code"]
            order.total = total
            order.tax_data = tax_data
            order.total_tax = tax
            order.payment_method = request.POST["payment_method"]
            # order number
            order.save()
            order.order_number = generate_order_number(order.id)
            order.save()
            messages.success(request, "Order Saved")
            return redirect("place_order")

        else:
            print(form.errors)
    context = {}
    return render(request, "orders/place_order.html", context)
