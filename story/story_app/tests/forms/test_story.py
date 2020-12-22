from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from story_app.forms import StoryForm
from story_app.models import Story
from story_auth.models import UserProfile, Writer


class StoryFormTests(TestCase):
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

        image = SimpleUploadedFile(name='test-image.jpg',
                                   content=open('story_app/tests/views/test-image.jpg', 'rb').read(),
                                   content_type='image/jpeg')

        form = StoryForm(
            data={
                'title': 'Test Story',
                'content': 'Lorem ipsum',
                'category': 'FN',
            },
            files={
                'image': image,
            })

        self.assertTrue(form.is_valid())
