from django.db import models
from account.models import User, UserProfile
from account.utils import send_notification

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
