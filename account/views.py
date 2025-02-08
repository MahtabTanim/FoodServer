from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils.html import format_html

from account.models import User
from .forms import UserForm
from django.contrib import messages

# Create your views here.


def registerUser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # create user using form
            # password = form.cleaned_data["password"]
            # user = form.save(commit=False)
            # user.role = 2
            # user.set_password(password)
            # user.save()
            # return redirect("registerUser")

            # create user using User model

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
            messages.success(request, "Your Account has been registered Successfully")
            return redirect("registerUser")
        else:
            print("form invalid")
            messages.error(request, "Invalid Form Submission")
    else:
        form = UserForm()

    context = {
        "form": form,
    }
    return render(request, "account/registerUser.html", context=context)
