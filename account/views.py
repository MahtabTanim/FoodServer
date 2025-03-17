from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils.html import format_html

from account.models import User, UserProfile
from orders.models import Order
from vendor.models import Vendor
from .forms import UserForm, VendorForm
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email, send_password_reset_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify


# Restrict Restaurant from accessing Customer Page
def check_restaurant(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict Customer from Accessing vendor
def check_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "you are already logged in")
        return redirect("myAccount")
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            user.role = 2
            user.save()

            # send Verification Email
            send_verification_email(request, user)
            messages.success(request, "Your Account has been registered Successfully")
            return redirect("login")
        else:
            messages.error(request, "Invalid Form Submission")
    else:
        form = UserForm()

    context = {
        "form": form,
    }
    return render(request, "account/registerUser.html", context=context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "you are already logged in")
        return redirect("myAccount")
    elif request.method == "POST":
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            user.role = 1
            user.save()
            messages.success(
                request, "Your User Account has been registered Successfully"
            )
            vendor_name = v_form.cleaned_data["vendor_name"]
            slug = slugify(vendor_name) + "-" + str(user.id)
            vendor_licesnse = v_form.cleaned_data["vendor_licesnse"]
            user_profile = UserProfile.objects.get(user=user)
            vendor = Vendor.objects.create(
                user=user,
                user_profile=user_profile,
                vendor_name=vendor_name,
                vendor_licesnse=vendor_licesnse,
                vendor_slug=slug,
            )
            vendor.save()
            # send verification email
            send_verification_email(request, user)
            messages.success(
                request,
                "Your Vendor Account has been registered Successfully , Please wait for the Approval",
            )
            return redirect("login")
        else:
            messages.error(request, "Invalid Vendor Form Submission")

    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        "form": form,
        "v_form": v_form,
    }
    return render(request, "account/registerVendor.html", context=context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "you are already logged in")
        return redirect("myAccount")
    elif request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("myAccount")
        else:
            messages.error(request, "Invalid Login Credential")
            return redirect("login")
    return render(request, "account/login.html")


def logout(request):
    auth.logout(request)
    messages.info(request, "You are Now Logged Out")
    return redirect("login")


@login_required(login_url="login")
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url="login")
@user_passes_test(check_customer)
def custDashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by(
        "-created_at"
    )
    context = {
        "orders": orders[:5],
        "total_orders": orders.count(),
    }
    return render(request, "account/custDashboard.html", context)


@login_required(login_url="login")
@user_passes_test(check_restaurant)
def restaurantDashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by(
        "-created_at"
    )
    context = {
        "orders": orders,
        "total_order": orders.count(),
        "recent_orders": orders[:5],
    }
    print(orders)
    return render(request, "account/restaurantDashboard.html", context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations your account is activated")
        return redirect("myAccount")
    else:
        messages.error(request, "Invalid activation Link")
        return redirect("myAccount")


def forgotpassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # send reset password email
            send_password_reset_email(request, user)
            messages.success(request, "Password reset email sent to email address")
            return redirect("myAccount")
        else:
            messages.error(request, "Account Does not Exists")
            return redirect("registerUser")
    return render(request, "account/forgotpassword.html")


def resetpassword_validate(request, uidb64, token):
    # validate the user
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.info(request, "Please reset Your Password")
        return redirect("resetpassword")
    else:
        messages.error(request, "Invalid Reset Link")
        return redirect("forgotpassword")


def resetpassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password and confirm_password and password == confirm_password:
            user = User.objects.get(pk=request.session["uid"])
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password reset Successfull")
            return redirect("login")
        else:
            messages.error(request, "Password reset UnSuccessfull")
            return redirect("resetpassword")
    return render(request, "account/resetpassword.html")
