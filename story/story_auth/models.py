from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return f'{self.user.username}'


class Writer(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    description = models.TextField(max_length=500, blank=True)

    @property
    def full_name(self):
        return f'{self.user_profile.user.first_name} {self.user_profile.user.last_name}'

    @property
    def first_name(self):
        return f'{self.user_profile.user.first_name}'

    @property
    def last_name(self):
        return f'{self.user_profile.user.last_name}'

    def __str__(self):
        return f'{self.full_name}'

