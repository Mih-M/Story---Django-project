from django.contrib import admin
from django.contrib.auth.models import Group

from story_app.admin import LikeInline, FavoriteInline, CommentInline
from story_auth.models import UserProfile, Writer


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [
        LikeInline,
        CommentInline,
        FavoriteInline,
    ]

    def status(self, obj):
        return 'Writer' if obj.user.groups.filter(name='Writer').exists() else 'User'

    list_display = ['user', 'status']


class WriterAdmin(admin.ModelAdmin):
    def total_stories(self, obj):
        return obj.story_set.count()

    def published_stories(self, obj):
        return obj.story_set.filter(published=True).count()

    def unpublished_stories(self, obj):
        return obj.story_set.filter(published=False).count()

    list_display = ['full_name', 'user_profile', 'approved', 'total_stories', 'published_stories', 'unpublished_stories']
    readonly_fields = ['approved']

    def approve(self, request, queryset):
        group = Group.objects.get(name='Writer')

        for writer in queryset:
            writer.user_profile.user.groups.add(group)

        count = queryset.update(approved=True)
        message = f'{count} writers have' if count > 1 else f'{count} writer has'
        self.message_user(request, f'{message} been approved.')

    approve.short_description = 'Approve selected writers'

    def disapprove(self, request, queryset):
        group = Group.objects.get(name='Writer')

        for writer in queryset:
            writer.user_profile.user.groups.remove(group)

        count = queryset.update(approved=False)
        message = f'{count} writers have' if count > 1 else f'{count} writer has'
        self.message_user(request, f'{message} been disapproved.')

    disapprove.short_description = 'Disapprove selected writers'

    actions = ['approve', 'disapprove']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Writer, WriterAdmin)
