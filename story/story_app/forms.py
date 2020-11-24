from django import forms

from story_app.models import Story


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('published', 'writer',)

