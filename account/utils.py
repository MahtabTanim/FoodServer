from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def detectUser(user):
    if user.role == 1:
        return "restaurantDashboard"

    if user.role == 2:
        return "custDashboard"

    if user.role == None and user.is_superadmin:
        return "/admin"


def send_verification_email(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_sub = "please activate your account"
    message = render_to_string(
        "account/emails/account_verification_email.html",
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email
    mail = EmailMessage(mail_sub, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()


def send_password_reset_email(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_sub = "Reset your Password"
    message = render_to_string(
        "account/emails/reset_password_email.html",
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email
    mail = EmailMessage(mail_sub, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email = context["user"].email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()
    print("Notification email sent")


def generate_total_by_vendor(orders, vendor):
    order_totals = dict()
    total_rev = 0
    for order in orders:
        tax_data = order.total_data[str(vendor.id)]
        t_data = {}
        for key, val in tax_data.items():
            subtotal = key
            t_data = val
        tax_data = t_data
        total_tax = 0
        for tax, data in order.tax_data.items():
            for key, val in data.items():
                total_tax += round(float(subtotal) * float(key) / 100, 2)
        total = round(float(subtotal) + float(total_tax), 2)
        total_rev += total
        order_totals.update({str(order): str(total)})
    return {
        "order_totals": order_totals,
        "total_rev": total_rev,
    }
