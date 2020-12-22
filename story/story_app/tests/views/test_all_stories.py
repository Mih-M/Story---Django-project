from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase, Client

from story_app.models import Story
from story_auth.models import UserProfile, Writer


class AllStoriesViewTests(TestCase):
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

        image = 'image.jpg'

        self.story1 = Story(writer=self.writer, title='Published Story', content='Lorem ipsum', category='FN', image=image)
        self.story1.full_clean()
        self.story1.published = True
        self.story1.save()

        self.story2 = Story(writer=self.writer, title='Unpublished Story', content='Lorem ipsum', category='FN', image=image)
        self.story2.full_clean()
        self.story2.save()

    def test_all_stories_no_user(self):
        response = self.client.get('/all-stories/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_stories.html')
        self.assertContains(response, 'Sign In')
        self.assertContains(response, 'Sign Up')
        self.assertContains(response, 'Published Story')
        self.assertNotContains(response, 'Unpublished Story')

    def test_all_stories_user(self):
        new_user = User.objects.create_user('Peter')
        new_user.set_password('1234')
        new_user.save()
        self.client.login(username='Peter', password='1234')
        response = self.client.get('/all-stories/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.username, 'Peter')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_stories.html')
        self.assertContains(response, 'Hello, Peter')
        self.assertContains(response, 'Sign Out')
        self.assertContains(response, 'Published Story')
        self.assertNotContains(response, 'Unpublished Story')
