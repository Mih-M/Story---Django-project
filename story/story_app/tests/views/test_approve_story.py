from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from story_app.models import Story
from story_auth.models import UserProfile, Writer


class ApproveStoryViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user = User(username='User1', first_name='Test', last_name='Writer')
        self.user.set_password('1234')
        self.user.full_clean()
        self.user.save()
        self.user_profile = UserProfile(user=self.user)
        self.user_profile.full_clean()
        self.user_profile.save()
        self.writer = Writer(user_profile=self.user_profile)
        self.writer.full_clean()
        self.writer.save()

        image = 'image.jpg'

        self.story = Story(writer=self.writer, title='Test Story', content='Lorem ipsum', category='FN', image=image)
        self.story.full_clean()
        self.story.save()

    def test_approve_story_no_user(self):
        response = self.client.get(f'/approve-story/{self.story.id}/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        self.assertRedirects(response, '/')

    def test_approve_story_user(self):
        new_user = User.objects.create_user('Peter')
        new_user.set_password('1234')
        new_user.save()

        new_user_profile = UserProfile(user=new_user)
        new_user_profile.full_clean()
        new_user_profile.save()

        self.client.login(username='Peter', password='1234')

        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.username, 'Peter')

        response = self.client.get(f'/approve-story/{self.story.id}/')
        self.assertRedirects(response, '/')

    def test_approve_story_superuser(self):
        superuser = User.objects.create_user('Superuser')
        superuser.set_password('1234')
        superuser.is_superuser = True
        superuser.save()

        self.client.login(username='Superuser', password='1234')

        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.is_superuser, True)

        self.assertFalse(self.story.published)

        response = self.client.post(f'/approve-story/{self.story.id}/')

        self.assertRedirects(response, reverse('su_profile'))

        self.story.refresh_from_db()

        self.assertTrue(self.story.published)
