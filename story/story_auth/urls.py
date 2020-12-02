from django.urls import path

from django.contrib.auth import views as auth_views

from story_auth.views import sign_up, sign_in, sign_out, profile, su_profile, become_a_writer, approve_writer, \
    edit_profile, delete_profile

urlpatterns = [
    path('sign-up/', sign_up, name='sing_up'),
    path('sign-in/', sign_in, name='sing_in'),
    path('sign-out/', sign_out, name='sing_out'),

    path('become-a-writer/', become_a_writer, name='become_a_writer'),

    path('profile/<slug:username>/', profile, name='profile'),
    path('edit-profile/<slug:username>/', edit_profile, name='edit_profile'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'),
         name='change_password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'),
         name='password_change_done'),
    path('delete-profile/<slug:username>/', delete_profile, name='delete_profile'),

    path('su-profile/', su_profile, name='su_profile'),
    path('approve-writer/<int:writer_pk>', approve_writer, name='approve_writer'),
]
