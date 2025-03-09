from django.http import HttpResponse
from django.shortcuts import render
from vendor.models import Vendor
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from geopy.distance import distance


def get_or_set_current_location(request):
    if "lat" in request.session:
        lat = request.session["lat"]
        lng = request.session["lng"]
        return lat, lng
    elif "lat" in request.GET:
        request.session["lat"] = request.GET["lat"]
        request.session["lng"] = request.GET["lng"]
        return request.GET["lat"], request.GET["lng"]
    return None


def home(request):
    if "lat" in request.GET or "lat" in request.session:
        lat, lng = get_or_set_current_location(request)
        pnt = GEOSGeometry(f"POINT({lng} {lat})", srid=4326)
        vendors = (
            Vendor.objects.filter(is_approved=True, user__is_active=True)
            .annotate(distance=Distance("user_profile__location", pnt))
            .order_by("-distance")  # Ensure ascending distance
        )[:8]
        for v in vendors:
            v.kms = round(v.distance.km, 1)
            # print(v.kms)
    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    context = {
        "vendors": vendors,
    }
    return render(request, "home.html", context=context)
