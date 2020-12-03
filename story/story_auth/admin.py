from django.contrib import admin

from story_app.admin import LikeInline, FavoriteInline, CommentInline
from story_auth.models import UserProfile, Writer


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [
        LikeInline,
        CommentInline,
        FavoriteInline,
    ]


class WriterAdmin(admin.ModelAdmin):
    def total_stories(self, obj):
        return obj.story_set.count()

    def published_stories(self, obj):
        return obj.story_set.filter(published=True).count()

    def unpublished_stories(self, obj):
        return obj.story_set.filter(published=False).count()

    list_display = ['full_name', 'user_profile', 'approved', 'total_stories', 'published_stories', 'unpublished_stories']

    def approve(self, request, queryset):
        count = queryset.update(approved=True)
        message = f'{count} writers have' if count > 1 else f'{count} writer has'
        self.message_user(request, f'{message} been approved.')

    approve.short_description = 'Approve selected writers'

    actions = ['approve']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Writer, WriterAdmin)
