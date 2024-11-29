from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FollowForm(forms.Form):
    user_to_follow = forms.CharField(max_length=150)

class MessageForm(forms.Form):
    receiver = forms.CharField(max_length=150)
    content = forms.CharField(widget=forms.Textarea)