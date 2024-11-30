from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # null=True로 설정
    solved_problems = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username if self.user else "No User"

class Problem(models.Model):
    title = models.CharField(max_length=100)  # 문제 제목
    description = models.TextField()  # 문제 설명
    options = models.TextField(null=True, blank=True)  # 선택지
    image_path = models.ImageField(upload_to='uploads/', null=True, blank=True)  # 이미지 파일
    category = models.CharField(max_length=50)  # 카테고리
    difficulty = models.CharField(max_length=20)  # 난이도
    tags = models.CharField(max_length=200, null=True, blank=True)  # 태그

    def __str__(self):
        return self.title