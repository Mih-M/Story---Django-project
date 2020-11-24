from django.contrib import admin

from story_auth.models import UserProfile, Writer

admin.site.register(UserProfile)
admin.site.register(Writer)
