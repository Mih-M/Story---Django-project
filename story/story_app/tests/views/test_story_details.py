from django.contrib import auth
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.test import TestCase, Client

from story_app.models import Story
from story_auth.models import Writer, UserProfile


class StoryDetailsViewTests(TestCase):
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

    def test_story_details_no_user(self):
        response = self.client.get(f'/story-details/{self.story.id}/{slugify(self.story.title)}/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'story_details.html')
        self.assertContains(response, f'{self.story.title}')
        self.assertContains(response, f'{self.story.writer}')
        self.assertContains(response, 'Like, comment and save your favorite stories.')
        self.assertContains(response, 'Sign In')
        self.assertContains(response, 'Sign Up')
        self.assertNotContains(response, 'Comment')
        self.assertNotContains(response, 'Edit')
        self.assertNotContains(response, 'Delete')

    def test_story_details_user(self):
        new_user = User.objects.create_user(username='Peter')
        new_user.set_password('1234')
        new_user.save()
        user_profile = UserProfile(user=new_user)
        user_profile.full_clean()
        user_profile.save()
        self.client.login(username='Peter', password='1234')
        response = self.client.get(f'/story-details/{self.story.id}/{slugify(self.story.title)}/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.username, 'Peter')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'story_details.html')
        self.assertContains(response, f'{self.story.title}')
        self.assertContains(response, f'{self.story.writer}')
        self.assertContains(response, 'Comment')
        self.assertContains(response, 'Hello, Peter')
        self.assertContains(response, 'Sign Out')
        self.assertNotContains(response, 'Edit')
        self.assertNotContains(response, 'Delete')

    def test_story_details_writer(self):
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
        response = self.client.get(f'/story-details/{self.story.id}/{slugify(self.story.title)}/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.username, 'Peter')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'story_details.html')
        self.assertContains(response, f'{self.story.title}')
        self.assertContains(response, f'{self.story.writer}')
        self.assertContains(response, 'Comment')
        self.assertContains(response, 'Hello, Peter')
        self.assertContains(response, 'Sign Out')
        self.assertContains(response, 'Edit')
        self.assertContains(response, 'Delete')
