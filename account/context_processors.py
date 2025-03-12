from vendor.models import Vendor
from django.conf import settings
from .models import User, UserProfile


def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
        return {"vendor": vendor}
    except:
        return {"vendor": None}


def get_customer(request):
    try:
        customer = User.objects.get(id=request.user.id, role=2)
        return {"customer": customer}
    except:
        return {"customer": None}


def get_user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        return {"user_profile": profile}
    except:
        return {"user_profile": None}


def google_api(request):
    return {"GOOGLE_API_KEY": settings.GOOGLE_API_KEY}
