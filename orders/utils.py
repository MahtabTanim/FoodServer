import datetime
from sslcommerz_lib import SSLCOMMERZ
from marketplace.context_processors import get_cart_counter
from orders.models import Order, OrderedFood
from account.models import UserProfile
from marketplace.models import Cart
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings as stngs
from django.db.models import Sum


def generate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%s")
    order_number = current_datetime + str(pk)
    return order_number[:20]


# Create a Initial Payment Request Session
settings = {
    "store_id": "tntco67d45a4dbaa25",
    "store_pass": "tntco67d45a4dbaa25@ssl",
    "issandbox": True,
}


def send_payment_request(request, order_id, url):
    sslcz = SSLCOMMERZ(settings)
    order = Order.objects.get(user=request.user, order_number=order_id)
    user_profile = UserProfile.objects.get(user=request.user)
    cart_items = Cart.objects.filter(user=request.user).order_by("-updated_at")
    product_names = ""
    product_categories = ""
    for cart in cart_items:
        product_names = product_names + cart.fooditem.food_title + ","
        product_categories = (
            product_categories + cart.fooditem.category.category_name + ","
        )
    post_body = {}
    post_body["total_amount"] = order.total
    post_body["currency"] = "BDT"
    post_body["tran_id"] = order_id
    post_body["success_url"] = url
    post_body["fail_url"] = url
    post_body["cancel_url"] = url
    post_body["emi_option"] = 0
    post_body["cus_name"] = request.user.first_name + request.user.last_name
    post_body["cus_email"] = request.user.email
    post_body["cus_phone"] = request.user.phone_number
    post_body["cus_add1"] = user_profile.address
    post_body["cus_city"] = user_profile.city
    post_body["cus_country"] = (
        user_profile.country if user_profile.country else "Bangladesh"
    )

    post_body["shipping_method"] = "NO"
    post_body["multi_card_name"] = ""
    post_body["num_of_item"] = get_cart_counter(request)["cart_count"]
    post_body["product_name"] = product_names
    post_body["product_category"] = product_categories
    post_body["product_profile"] = "general"
    response = sslcz.createSession(post_body)  # API response
    return response
    # Need to redirect user to response['GatewayPageURL']


def send_notification(mail_subject, mail_template, context):
    from_email = stngs.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email = context["to_email"]
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()
    print("Notification email sent")


# {vendorid : {"subtotal" : {tax_data}}}
def vendors_pecific_tax_details(order_number, vendors, tax_data):
    tax_dict = {}
    order = Order.objects.get(order_number=order_number)
    for vendor in vendors:
        ordered_foods = OrderedFood.objects.filter(order=order, fooditem__vendor=vendor)
        subtotal = ordered_foods.aggregate(Sum("amount"))["amount__sum"]
        tax_data = {}
        for tax, data in order.tax_data.items():
            for key, val in data.items():
                tax_data.update(
                    {tax: {str(key): str(round(float(subtotal) * float(key) / 100, 2))}}
                )
        tax_dict.update({str(vendor.id): {str(subtotal): tax_data}})
    return tax_dict
