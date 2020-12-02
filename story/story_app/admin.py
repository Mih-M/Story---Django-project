from django.contrib import admin

from story_app.models import Story, Comment


class LikeInline(admin.TabularInline):
    model = Story.likes.through
    extra = 1
    verbose_name = 'Likes'


class FavoriteInline(admin.TabularInline):
    model = Story.favorites.through
    extra = 1


class StoryAdmin(admin.ModelAdmin):
    inlines = [
        LikeInline,
        FavoriteInline,
    ]
    exclude = ('likes', 'favorites',)


admin.site.register(Story, StoryAdmin)
admin.site.register(Comment)
