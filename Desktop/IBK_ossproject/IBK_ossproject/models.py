from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    solved_problems = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username if self.user else "No User"

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friends1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friends2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.username} is friends with {self.user2.username}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

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

    CATEGORY_CHOICES = [
        ('알고리즘', '알고리즘'),
        ('자료구조', '자료구조'),
        ('프로그래밍 언어', '프로그래밍 언어'),
        ('기타', '기타'),
    ]

    title = models.CharField(max_length=255)  # 문제 제목
    description = models.TextField()  # 문제 설명
    options = models.JSONField(default=list, blank=True, null=True)  # 선택지 (JSON 형식으로 저장)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True)  # 카테고리
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)  # 난이도
    tags = models.CharField(max_length=255, blank=True, null=True)  # 태그
    image = models.ImageField(upload_to='problem_images/', blank=True, null=True)  # 이미지
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problems_created')  # 작성자
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일

    def __str__(self):
        return self.title

class Question(models.Model):
    CATEGORY_CHOICES = [
        ('알고리즘', '알고리즘'),
        ('자료구조', '자료구조'),
        ('프로그래밍 언어', '프로그래밍 언어'),
        ('기타', '기타'),
    ]
    DIFFICULTY_CHOICES = [
        ('쉬움', '쉬움'),
        ('보통', '보통'),
        ('어려움', '어려움'),
    ]

    title = models.CharField(max_length=255)  # 질문 제목
    content = models.TextField()  # 질문 내용
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True)  # 카테고리
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, blank=True, null=True)  # 난이도
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions_created')  # 작성자
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일

    def __str__(self):
        return self.title


class Data(models.Model):
    CATEGORY_CHOICES = [
        ('알고리즘', '알고리즘'),
        ('자료구조', '자료구조'),
        ('프로그래밍 언어', '프로그래밍 언어'),
        ('기타', '기타'),
    ]

    title = models.CharField(max_length=255)  # 질문 제목
    content = models.TextField(default="기본 내용 없음")  # 질문 내용, 기본값 설정
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True)  # 카테고리
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data_posts')  # 작성자
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일

    def __str__(self):
        return self.title
