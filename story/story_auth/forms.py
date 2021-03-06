from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email', False)
        if not email:
            raise forms.ValidationError('Email is required')

        return email


class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class BecomeAWriterForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    picture = forms.ImageField(required=False)


class EditProfileWriterForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    picture = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 20, 'rows': 5}
    ), max_length=500, required=False)


class EditProfileUserForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    picture = forms.ImageField(required=False)


