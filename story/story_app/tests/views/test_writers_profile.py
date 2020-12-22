from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.test import TestCase, Client

from story_auth.models import Writer, UserProfile


class WritersProfileViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        user = User(username='User', password='1234', first_name='Test', last_name='Writer')
        user.full_clean()
        user.save()
        user_profile = UserProfile(user=user)
        user_profile.full_clean()
        user_profile.save()
        self.writer = Writer(user_profile=user_profile)
        self.writer.full_clean()
        self.writer.save()

    def test_writers_profile(self):
        response = self.client.get(f'/writers-profile/{self.writer.id}/{slugify(self.writer.full_name)}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'writers_profile.html')
        self.assertContains(response, 'Test Writer')
        self.assertContains(response, 'Test Writer\'s stories')

