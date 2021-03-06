from django.contrib import auth
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.test import TestCase, Client

from story_app.models import Story
from story_auth.models import UserProfile, Writer


class LikeStoryViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        user = User(username='User', password='1234', first_name='Test', last_name='Writer')
        user.full_clean()
        user.save()
        user_profile = UserProfile(user=user)
        user_profile.full_clean()
        user_profile.save()
        writer = Writer(user_profile=user_profile)
        writer.full_clean()
        writer.save()
        img = 'image.jpg'
        self.story = Story(writer=writer, title='Test Story', content='Lorem ipsum', category='FN', image=img)
        self.story.full_clean()
        self.story.published = True
        self.story.save()

    def test_like_no_user(self):
        response = self.client.get(f'/like-story/{self.story.id}/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        self.assertEqual(response.status_code, 302)

    def test_like_writer(self):
        new_user = User.objects.create_user(username='Peter', first_name='Peter', last_name='Petrov')
        new_user.set_password('1234')
        new_user.save()
        user_profile = UserProfile(user=new_user)
        user_profile.full_clean()
        user_profile.save()
        writer = Writer(user_profile=user_profile)
        writer.full_clean()
        writer.save()
        self.story.writer = writer
        self.story.save()

        self.client.login(username='Peter', password='1234')

        response = self.client.get(f'/like-story/{self.story.id}/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertRedirects(response, '/')

    def test_like_user(self):
        new_user = User.objects.create_user(username='Peter')
        new_user.set_password('1234')
        new_user.save()
        user_profile = UserProfile(user=new_user)
        user_profile.full_clean()
        user_profile.save()

        self.client.login(username='Peter', password='1234')

        response = self.client.get(f'/like-story/{self.story.id}/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.username, 'Peter')
        self.assertRedirects(response, f'/story-details/{self.story.id}/{slugify(self.story.title)}/')
        self.assertEqual(len(self.story.likes.all()), 1)

    def test_unlike_user(self):
        new_user = User.objects.create_user(username='Peter')
        new_user.set_password('1234')
        new_user.save()
        user_profile = UserProfile(user=new_user)
        user_profile.full_clean()
        user_profile.save()

        self.story.like_set.create(user_profile=user_profile)

        self.client.login(username='Peter', password='1234')

        response = self.client.get(f'/like-story/{self.story.id}/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.username, 'Peter')
        self.assertRedirects(response, f'/story-details/{self.story.id}/{slugify(self.story.title)}/')
        self.assertEqual(len(self.story.likes.all()), 0)
