from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile_reciever(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)


# @receiver(pre_save, sender=User)
# def pre_save_profile_reciever(sender, instance, **kwargs):
#     print(instance.username, " this username is being created")


# post_save.connect(post_save_create_profile_reciever ,sender =User)
