from django.urls import path

from story_app.views import home, all_stories, story_details, add_story, writers_profile, custom_stories, edit_story, \
    approve_story, delete_story

urlpatterns = [
    path('', home, name='home'),
    path('all/', all_stories, name='all_stories'),
    path('custom_stories/<slug:username>/<str:request_stories>/', custom_stories, name='custom_stories'),
    path('story_details/<int:pk>/<slug:story_title>', story_details, name='story_details'),
    path('add_story', add_story, name='add_story'),
    path('writers_profile/<int:pk>/<slug:writers_name>/', writers_profile, name='writers_profile'),
    path('edit_story/<int:story_pk>/<slug:story_title>', edit_story, name='edit_story'),
    path('delete_story/<int:story_pk>/<slug:story_title>', delete_story, name='delete_story'),
    path('approve_story/<int:story_pk>/', approve_story, name='approve_story'),
]
