from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
<<<<<<< Updated upstream
=======
from .models import BlogPost
from .models import Problem
>>>>>>> Stashed changes

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
<<<<<<< Updated upstream
=======

class FollowForm(forms.Form):
    user_to_follow = forms.CharField(max_length=150)

class MessageForm(forms.Form):
    receiver = forms.CharField(max_length=150)
    content = forms.CharField(widget=forms.Textarea)

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # user를 kwargs에서 꺼내옵니다.
        super(BlogPostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(BlogPostForm, self).save(commit=False)
        if self.user:
            instance.author = self.user  # author를 현재 사용자로 설정합니다.
        if commit:
            instance.save()
        return instance
    
class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'category', 'difficulty', 'tags', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '문제 제목을 입력하세요'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '문제 설명을 입력하세요'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '카테고리를 입력하세요'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '태그를 쉼표로 구분하여 입력하세요'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
>>>>>>> Stashed changes
