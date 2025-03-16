from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from account.forms import UserProfileForm, UserInfoForm
from account.views import check_customer
from account.context_processors import get_customer, get_user_profile
from django.shortcuts import get_object_or_404
from account.models import UserProfile, User
from django.contrib import messages

from orders.models import Order, OrderedFood


@login_required(login_url="login")
@user_passes_test(check_customer)
def cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    user = get_object_or_404(User, id=request.user.id)
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile and User Updated")
            return redirect("cprofile")
        else:
            context = {
                "profile_form": profile_form,
                "user_form": user_form,
            }
            return render(request, "vendor/vprofile.html", context)
    else:

        profile_from = UserProfileForm(instance=profile)
        userForm = UserInfoForm(instance=user)

        context = {
            "profile_form": profile_from,
            "user_form": userForm,
        }
        return render(request, "customers/cprofile.html", context)


@login_required(login_url="login")
@user_passes_test(check_customer)
def myorders(request):
    print(request.path)
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by(
        "-created_at"
    )
    context = {
        "orders": orders,
        "total_orders": orders.count(),
    }
    return render(request, "customers/myorders.html", context)


def order_details(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
        ordered_foods = OrderedFood.objects.filter(order=order)
        context = {
            "order": order,
            "ordered_foods": ordered_foods,
            "subtotal": order.total - order.total_tax,
            "tax_dictionary": order.tax_data,
        }
    except:
        return redirect("custDashboard")
    return render(request, "customers/order_details.html", context)
