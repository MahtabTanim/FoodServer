from django.contrib import admin
from .models import Vendor, OpeningHour

# Register your models here.


class VendorManager(admin.ModelAdmin):
    list_display = ["user", "vendor_name", "is_approved", "created_at"]
    list_display_links = ["user", "vendor_name"]


class OpeningHourManager(admin.ModelAdmin):
    list_display = ["vendor", "day", "from_hour", "to_hour", "is_closed"]
    list_editable = [
        "is_closed",
    ]


admin.site.register(OpeningHour, OpeningHourManager)
admin.site.register(Vendor, VendorManager)
