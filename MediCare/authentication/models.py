from __future__ import unicode_literals
import urllib
import hashlib
import os.path

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=50, null=True, blank=True)
    # reputation = models.IntegerField(default=0)
    # language = models.CharField(max_length=5, default='en')

    class Meta:
        db_table = 'auth_profile'


    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
