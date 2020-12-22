from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from django.test import TestCase, Client

from story_app.models import Story
from story_auth.models import UserProfile, Writer


class CustomStoriesViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        group = Group.objects.create(name='Writer')

        self.user1 = User(username='User1', first_name='Test', last_name='Writer1')
        self.user1.set_password('1234')
        self.user1.full_clean()
        self.user1.save()
        self.user1.groups.add(group)        #
        self.user1.save()

        self.user_profile1 = UserProfile(user=self.user1)
        self.user_profile1.full_clean()
        self.user_profile1.save()
        self.writer1 = Writer(user_profile=self.user_profile1)
        self.writer1.full_clean()
        self.writer1.save()

        self.user2 = User(username='User2', first_name='Test', last_name='Writer2')
        self.user2.set_password('1234')
        self.user2.full_clean()
        self.user2.save()
        self.user_profile2 = UserProfile(user=self.user2)
        self.user_profile2.full_clean()
        self.user_profile2.save()
        self.writer2 = Writer(user_profile=self.user_profile2)
        self.writer2.full_clean()
        self.writer2.save()

        image = 'image.jpg'

        self.story1 = Story(writer=self.writer1, title='Published Story', content='Lorem ipsum', category='FN', image=image)
        self.story1.full_clean()
        self.story1.published = True
        self.story1.save()

        self.story2 = Story(writer=self.writer1, title='Unpublished Story', content='Lorem ipsum', category='FN', image=image)
        self.story2.full_clean()
        self.story2.save()

        self.story3 = Story(writer=self.writer1, title='Favorite Story', content='Lorem ipsum', category='FN',
                            image=image)
        self.story3.full_clean()
        self.story3.published = True
        self.story3.save()

    def test_custom_stories_no_user(self):
        response = self.client.get(f'/custom-stories/{slugify(self.user1.username)}/{"favorite-stories"}/')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        self.assertEqual(response.status_code, 302)

    def test_custom_stories_user_favorite_stories(self):
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

        response = self.client.get(f'/custom-stories/{slugify(user.username)}/{"favorite-stories"}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_stories.html')
        self.assertContains(response, 'Hello, Peter')
        self.assertContains(response, 'Sign Out')
        self.assertNotContains(response, 'Favorite Story')

        new_user_profile.favorite_set.create(story=self.story3)

        response = self.client.get(f'/custom-stories/{slugify(user.username)}/{"favorite-stories"}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_stories.html')
        self.assertContains(response, 'Hello, Peter')
        self.assertContains(response, 'Sign Out')
        self.assertContains(response, 'Favorite Story')

    def test_custom_stories_user_wrong_request(self):
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

        response = self.client.get(f'/custom-stories/{slugify(user.username)}/{"my-stories"}/')
        self.assertRedirects(response, '/')

        response = self.client.get(f'/custom-stories/{slugify(user.username)}/{"unpublished-stories"}/')
        self.assertRedirects(response, '/')

        response = self.client.get(f'/custom-stories/{slugify(user.username)}/{"something else"}/')
        self.assertRedirects(response, '/')

    def test_custom_stories_writer_favorite_stories(self):
        self.client.login(username='User1', password='1234')

        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.username, 'User1')
        self.assertEqual(user.last_name, 'Writer1')

        response = self.client.get(f'/custom-stories/{slugify(user.username)}/{"favorite-stories"}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_stories.html')
        self.assertContains(response, 'Hello, User1')
        self.assertContains(response, 'Sign Out')
        self.assertNotContains(response, 'Favorite Story')

        self.user_profile1.favorite_set.create(story=self.story3)

        response = self.client.get(f'/custom-stories/{slugify(user.username)}/{"favorite-stories"}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_stories.html')
        self.assertContains(response, 'Hello, User1')
        self.assertContains(response, 'Sign Out')
        self.assertContains(response, 'Favorite Story')

    def test_custom_stories_writer_my_stories(self):
        self.client.login(username='User1', password='1234')

        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.username, 'User1')
        self.assertEqual(user.last_name, 'Writer1')

        response = self.client.get(f'/custom-stories/{slugify(user.username)}/{"my-stories"}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_stories.html')
        self.assertContains(response, 'Hello, User1')
        self.assertContains(response, 'Sign Out')
        self.assertContains(response, 'Published Story')

    def test_custom_stories_writer_unpublished_stories(self):
        self.client.login(username='User1', password='1234')

        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.username, 'User1')
        self.assertEqual(user.last_name, 'Writer1')

        response = self.client.get(f'/custom-stories/{slugify(user.username)}/{"unpublished-stories"}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_stories.html')
        self.assertContains(response, 'Hello, User1')
        self.assertContains(response, 'Sign Out')
        self.assertContains(response, 'Unpublished Story')
