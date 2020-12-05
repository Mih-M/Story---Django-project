from django.contrib import admin

from story_app.models import Story, Comment, Like, Favorite


class LikeInline(admin.StackedInline):
    model = Like
    extra = 1
    classes = ('collapse',)


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1
    classes = ('collapse',)


class FavoriteInline(admin.StackedInline):
    model = Favorite
    extra = 1
    classes = ('collapse',)


class StoryAdmin(admin.ModelAdmin):
    inlines = [
        LikeInline,
        CommentInline,
        FavoriteInline,
    ]

    fieldsets = [
        ('Story information', {'fields': ('title', 'category', 'published', 'writer')}),
        ('Additional information', {'fields': ('content', 'image'), 'classes': ('collapse',)}),
    ]

    def total_likes(self, obj):
        return obj.like_set.count()

    def total_comments(self, obj):
        return obj.comment_set.count()

    def added_to_favorites(self, obj):
        return obj.favorite_set.count()

    def publish(self, request, queryset):
        count = queryset.update(published=True)
        message = f'{count} stories have' if count > 1 else f'{count} story has'
        self.message_user(request, f'{message} been published successfully.')

    publish.short_description = 'Mark selected stories as published'

    list_display = ['title', 'writer', 'total_likes', 'total_likes', 'added_to_favorites', 'published']
    list_filter = ['writer']
    search_fields = ['title']
    actions = ['publish']


class LikeAdmin(admin.ModelAdmin):
    def story_title(self, obj):
        return obj.story.title

    list_display = ['story_title', 'user_profile']


class CommentAdmin(admin.ModelAdmin):
    def story_title(self, obj):
        return obj.story.title

    list_display = ['story_title', 'author']


class FavoriteAdmin(admin.ModelAdmin):
    def story_title(self, obj):
        return obj.story.title

    list_display = ['story_title', 'user_profile']


admin.site.register(Story, StoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
