from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase, Client


class HomeViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_home_no_user(self):
        response = self.client.get('')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Like, comment and save your favorite stories.')
        self.assertContains(response, 'Sign In')
        self.assertContains(response, 'Sign Up')

    def test_home_user(self):
        new_user = User.objects.create_user('Peter')
        new_user.set_password('1234')
        new_user.save()
        self.client.login(username='Peter', password='1234')
        response = self.client.get('')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.username, 'Peter')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Latest stories')
        self.assertContains(response, 'Hello, Peter')
        self.assertContains(response, 'Sign Out')
