from django.contrib import admin

from story_app.admin import LikeInline, FavoriteInline
from story_auth.models import UserProfile, Writer


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [
        LikeInline,
        FavoriteInline,
    ]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Writer)
