from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from story_app.models import Story
from story_auth.models import UserProfile, Writer


class StoryModelTests(TestCase):
    def test_create_story(self):
        user = User(username='User', password='1234')
        user.full_clean()
        user.save()
        user_profile = UserProfile(user=user)
        user_profile.full_clean()
        user_profile.save()
        writer = Writer(user_profile=user_profile)
        writer.full_clean()
        writer.save()
        img = 'image.jpg'
        story = Story(writer=writer, title='Test Story', content='Lorem ipsum', category='FN', image=img)
        story.full_clean()
        story.save()

        self.assertEqual(story.title, 'Test Story')
        self.assertEqual(story.content, 'Lorem ipsum')
        self.assertEqual(story.writer, writer)
        self.assertEqual(story.category, 'FN')
        self.assertEqual(story.image, img)
        self.assertEqual(story.date, date.today())
        self.assertEqual(len(story.like_set.all()), 0)
        self.assertEqual(len(story.favorite_set.all()), 0)
        self.assertEqual(len(story.comment_set.all()), 0)
        self.assertFalse(story.published)

