from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)  # 제목
    content = models.TextField()  # 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일
    image_url = models.URLField(blank=True, null=True)  # 이미지 URL (선택사항)

    def __str__(self):
        return self.title
