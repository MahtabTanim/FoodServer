from django.db import models
from account.models import User, UserProfile
from account.utils import send_notification
from datetime import time, date, datetime

# Create your models here.


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    user_profile = models.OneToOneField(
        UserProfile, related_name="userprofile", on_delete=models.CASCADE
    )
    vendor_name = models.CharField(max_length=100)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_licesnse = models.ImageField(upload_to="vendor/vendor_licesnse")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def is_open(self):
        is_open = None
        current_openings = OpeningHour.objects.filter(
            vendor=self, day=date.today().isoweekday()
        )
        current_time = datetime.now().strftime("%H:%M:%S")
        for i in current_openings:
            start_time = str(datetime.strptime(i.from_hour, "%I:%M %p").time())
            end_time = str(datetime.strptime(i.to_hour, "%I:%M %p").time())

            if current_time >= start_time and current_time <= end_time:
                is_open = True
                break
            else:
                is_open = False
        return is_open

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = Vendor.objects.get(pk=self.pk)
            if original.is_approved != self.is_approved:
                # send notification Email
                mail_template = "account/emails/restaurant_approval_rejection.html"
                context = {
                    "is_approved": self.is_approved,
                    "user": self.user,
                }
                if self.is_approved == True:
                    mail_subject = "Account Approval"
                    send_notification(mail_subject, mail_template, context)
                else:
                    mail_subject = "Account Rejection"
                    send_notification(mail_subject, mail_template, context)

        return super(Vendor, self).save(*args, **kwargs)


DayChoice = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]
HourChoice = [
    (time(h, m).strftime("%I:%M %p"), time(h, m).strftime("%I:%M %p"))
    for h in range(0, 24)
    for m in (0, 30)
]


class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(blank=True, null=True, choices=DayChoice)
    from_hour = models.CharField(blank=True, null=True, choices=HourChoice)
    to_hour = models.CharField(blank=True, null=True, choices=HourChoice)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ["day", "-from_hour"]
        unique_together = ["vendor", "day", "from_hour", "to_hour"]

    def __str__(self):
        return self.get_day_display()
