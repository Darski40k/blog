from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserCreateForm(UserCreationForm):

    email = forms.EmailField(label='Email Address', required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):

    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfilePicture(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['profile_picture']


class PasswordCheck(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
