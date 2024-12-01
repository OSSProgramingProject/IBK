from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BlogPost
from .models import Problem
from .models import Question
from .models import Data



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
        fields = ['title', 'description', 'difficulty', 'tags', 'image']  # 실제 모델 필드만 사용

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': '문제에 대한 설명을 입력하세요'}),
            'tags': forms.TextInput(attrs={'placeholder': '쉼표로 태그를 구분하여 입력하세요 (예: 태그1, 태그2)'}),
        }
    def __init__(self, *args, **kwargs):
        # kwargs에서 user를 꺼내 저장
        self.user = kwargs.pop('user', None)
        super(ProblemForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ProblemForm, self).save(commit=False)
        # 현재 사용자를 작성자로 설정
        if self.user:
            instance.author = self.user
        if commit:
            instance.save()
        return instance
    


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        # 모델에 실제 존재하는 필드만 사용합니다.
        fields = ['title', 'category', 'difficulty', 'content']  # 'content' 필드 추가

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '질문의 제목을 입력하세요'}),
            'category': forms.Select(),
            'difficulty': forms.Select(),
            'content': forms.Textarea(attrs={'placeholder': '질문 내용을 입력하세요', 'rows': 10}),  # 'content' 필드에 위젯 추가
        }

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['title', 'category', 'content']
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '질문의 제목을 입력하세요'}),
            'category': forms.Select(),
            'content': forms.Textarea(attrs={'placeholder': '질문 내용을 입력하세요', 'rows': 10}),  # 'content' 필드에 위젯 추가
        }