from .models import Profile, User
from django.db.models.signals import post_save

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, picture='../static/images/default.png')
        print("profile created !")

post_save.connect(create_profile, sender=User)

def update_profile(sender, instance, created, **kwargs):

    if created == False:
        instance.profile.save()
        print("Profile updated !")    

post_save.connect(update_profile, sender=User)