from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # null=True로 설정
    solved_problems = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username if self.user else "No User"

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friends1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friends2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', '쉬움'),
        ('Medium', '중간'),
        ('Hard', '어려움'),
    ]

    title = models.CharField(max_length=255)  # 문제 제목
    description = models.TextField()  # 문제 설명
    options = models.JSONField(default=list)  # 선택지를 JSON으로 저장
    category = models.CharField(max_length=100, blank=True, null=True)  # 카테고리
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES)  # 난이도
    tags = models.CharField(max_length=255, blank=True, null=True)  # 태그
    image = models.ImageField(upload_to='problem_images/', blank=True, null=True)  # 이미지
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problems')  # 작성자
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일

    def __str__(self):
        return self.title