from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from account.forms import UserProfileForm, UserInfoForm
from account.views import check_customer
from account.context_processors import get_customer, get_user_profile
from django.shortcuts import get_object_or_404
from account.models import UserProfile, User
from django.contrib import messages


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
