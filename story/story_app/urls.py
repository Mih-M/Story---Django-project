from django.urls import path

from story_app.views import home, all_stories, story_details, add_story, writers_profile, custom_stories, edit_story, \
    approve_story, delete_story, add_comment, like_story, add_to_favorites

urlpatterns = [
    path('', home, name='home'),
    path('all-stories/', all_stories, name='all_stories'),
    path('custom-stories/<slug:username>/<str:request_stories>/', custom_stories, name='custom_stories'),
    path('story-details/<int:story_pk>/<slug:story_title>', story_details, name='story_details'),

    path('add-story', add_story, name='add_story'),
    path('writers-profile/<int:writer_pk>/<slug:writers_name>/', writers_profile, name='writers_profile'),
    path('edit-story/<int:story_pk>/<slug:story_title>', edit_story, name='edit_story'),
    path('delete-story/<int:story_pk>/<slug:story_title>', delete_story, name='delete_story'),
    path('approve-story/<int:story_pk>/', approve_story, name='approve_story'),
    path('add-comment/<int:story_pk>/', add_comment, name='add_comment'),
    path('like-story/<int:story_pk>/', like_story, name='like_story'),
    path('add-to-favorites/<int:story_pk>/', add_to_favorites, name='add_to_favorites'),
]
