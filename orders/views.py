from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from marketplace.forms import OrderForm
from marketplace.models import Cart
from marketplace.context_processors import get_cart_total
from orders.utils import generate_order_number
from .models import Order
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user
from .utils import send_payment_request, vendors_pecific_tax_details
from django.views.decorators.csrf import csrf_exempt
from .models import Payment, OrderedFood
from django.contrib.sessions.models import Session
from .utils import send_notification


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
            context = {
                "order": order,
                "cart_items": cart_items,
            }
            return render(request, "orders/place_order.html", context)

        else:
            print(form.errors)
    context = {}
    return render(request, "orders/place_order.html", context)


def order(request, order_id=None):
    url = request.build_absolute_uri(reverse("status"))
    response = send_payment_request(request, order_id, url)
    return redirect(response["GatewayPageURL"])


@csrf_exempt
def status(request):
    if request.method == "POST" or request.method == "post":
        response = request.POST
        order = Order.objects.get(order_number=response["tran_id"])
        user = order.user
        if response["status"] == "VALID":
            # When the payment is successfull
            # store payment details in Payment model
            payment = Payment(
                user=user,
                transaction_id=response["bank_tran_id"],
                payment_method=response["card_type"],
                amount=response["amount"],
                status=response["status"],
            )
            payment.save()
            order.payment = payment
            # $######
            order.payment_method = response["card_type"]
            order.is_ordered = True
            order.save()
            # MOVE THE CART ITEMS TO ORDERED FOOD MODEL
            cart_items = Cart.objects.filter(user=user)
            total = 0
            vendors = list(set(item.fooditem.vendor for item in cart_items))
            order.vendors.set(vendors)
            for item in cart_items:
                ordered_food = OrderedFood(
                    order=order,
                    payment=payment,
                    user=item.user,
                    fooditem=item.fooditem,
                    quantity=item.quantity,
                    price=item.fooditem.price,
                    amount=item.fooditem.price * item.quantity,
                )
                total += item.quantity
                ordered_food.save()

            # vendor specific details
            # {vendorid : {"subtotal" : {tax_data}}}
            order.total_data = vendors_pecific_tax_details(
                order.order_number, vendors, order.tax_data
            )
            order.save()
            # SEND ORDER CONFIRMATION EMAIL TO THE CUSTOMER
            mail_subject = "Your order has been Confirmed"
            mail_template = "orders/emails/order_confirmed_email.html"
            context = {
                "user": user,
                "order": order,
                "cart_items": cart_items,
                "to_email": order.email,
                "total_items": total,
                "total": order.total,
                "tax_data": order.tax_data,
            }
            send_notification(mail_subject, mail_template, context)
            # SEND ORDER RECEIVED EMAIL TO THE VENDOR
            mail_subject = "New order recieved"
            mail_template = "orders/emails/order_recieved_email.html"
            for vendor in vendors:
                cart_items = Cart.objects.filter(fooditem__vendor=vendor, user=user)
                vendor_total_details = order.total_data.get(str(vendor.id))
                total_percentage = 0.0
                total = 0.0
                tax_data = {}
                for key, val in vendor_total_details.items():
                    total = key
                    tax_data = val
                    for k, percentage in tax_data.items():
                        for x, y in percentage.items():
                            total_percentage += float(x)
                total_with_tax = round(
                    float(total) + (float(total) * float(total_percentage) / 100), 2
                )
                print(total_with_tax)
                context = {
                    "vendor": vendor,
                    "order": order,
                    "cart_items": cart_items,
                    "to_email": vendor.user.email,
                    "total": total,
                    "tax_data": tax_data,
                    "total_with_tax": total_with_tax,
                }
                send_notification(mail_subject, mail_template, context)
            # CLEAR THE CART IF THE PAYMENT IS SUCCESS
            Cart.objects.filter(user=user).delete()
            return redirect("ssl_complete", response["val_id"], response["tran_id"])

        else:
            return HttpResponse("Payment Failed")
    return HttpResponse("Hello world")


def ssl_complete(request, val_id, tran_id):
    order = Order.objects.get(order_number=tran_id)
    ordered_foods = OrderedFood.objects.filter(order=order)
    context = {
        "order": order,
        "ordered_foods": ordered_foods,
        "subtotal": round(order.total - order.total_tax, 2),
        "tax_dictionary": order.tax_data,
    }
    return render(request, "orders/order_complete.html", context)
