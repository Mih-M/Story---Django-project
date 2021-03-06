from django import forms

from story_app.models import Story, Comment


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('writer', 'date', 'published', 'favorites', 'likes', 'comments')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {'content': forms.TextInput(
            attrs={'placeholder': 'Write your comment here...'}
        )}



