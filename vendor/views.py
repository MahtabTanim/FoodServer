from django.http import HttpResponse
from django.shortcuts import render
from account.forms import UserProfileForm, VendorForm
from django.shortcuts import get_object_or_404, redirect
from .models import Vendor
from account.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from account.views import check_restaurant


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
