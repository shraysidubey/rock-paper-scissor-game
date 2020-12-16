from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    wins = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username