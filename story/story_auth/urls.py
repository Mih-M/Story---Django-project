from django.urls import path

from story_auth.views import sign_up, sign_in, sign_out, profile, su_profile, become_a_writer, approve_writer

urlpatterns = [
    path('sign_up/', sign_up, name='sing_up'),
    path('sign_in/', sign_in, name='sing_in'),
    path('sign_out/', sign_out, name='sing_out'),
    path('become_a_writer/', become_a_writer, name='become_a_writer'),
    path('profile/<slug:username>', profile, name='profile'),
    path('su_profile/', su_profile, name='su_profile'),
    path('approve_writer/<int:pk>', approve_writer, name='approve_writer'),
]
