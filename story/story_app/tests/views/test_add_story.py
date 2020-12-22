from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.defaultfilters import slugify
from django.test import TestCase, Client

from story_app.forms import StoryForm
from story_app.models import Story
from story_auth.models import UserProfile, Writer


class AddStoryViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user = User(username='User', first_name='Test', last_name='Writer')
        self.user.set_password('1234')
        self.user.full_clean()
        self.user.save()
        self.user_profile = UserProfile(user=self.user)
        self.user_profile.full_clean()
        self.user_profile.save()
        self.writer = Writer(user_profile=self.user_profile)
        self.writer.full_clean()
        self.writer.save()

    def test_add_story_no_user(self):
        response = self.client.post('/add-story/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        self.assertRedirects(response, '/')

    def test_add_story_user(self):
        new_user = User.objects.create_user(username='Peter')
        new_user.set_password('1234')
        new_user.save()
        user_profile = UserProfile(user=new_user)
        user_profile.full_clean()
        user_profile.save()

        self.client.login(username='Peter', password='1234')

        response = self.client.get(f'/add-story/')

        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertRedirects(response, '/')

    def test_add_story_writer_not_approved_get(self):
        self.client.login(username='User', password='1234')

        response = self.client.get(f'/add-story/')

        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.username, 'User')

        self.assertRedirects(response, '/')

    def test_add_story_writer_not_approved_post(self):
        self.client.login(username='User', password='1234')

        response = self.client.post(f'/add-story/')

        self.assertRedirects(response, '/')

    def test_add_story_writer_approved_get(self):
        group = Group.objects.create(name='Writer')

        self.user.groups.add(group)

        self.client.login(username='User', password='1234')

        response = self.client.get(f'/add-story/')

        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.username, 'User')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_story.html')
        self.assertContains(response, 'Add new story')
        self.assertIsInstance(response.context['story_form'], StoryForm)

    def test_add_story_writer_approved_post(self):
        group = Group.objects.create(name='Writer')

        self.user.groups.add(group)

        self.client.login(username='User', password='1234')

        image = SimpleUploadedFile(name='test-image.jpg',
                                   content=open('story_app/tests/views/test-image.jpg', 'rb').read(),
                                   content_type='image/jpeg')

        response = self.client.post(f'/add-story/', data={
            'title': 'Test Story',
            'category': 'FN',
            'image': image,
            'content': 'Lorem ipsum',
        })

        self.assertRedirects(response, f'/auth/profile/{slugify(self.user.username)}/')

        self.assertEqual(len(self.writer.story_set.all()), 1)
        self.assertIn(Story.objects.get(title='Test Story'), self.writer.story_set.all())
        self.assertFalse(Story.objects.get(title='Test Story').published)

