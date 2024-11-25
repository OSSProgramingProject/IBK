from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 홈 페이지
    path('login/', views.user_login, name='login'),  # 로그인 페이지 - 사용자 정의함수 사용
    #path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'), # 로그인 페이지- Django 내장 로그인 뷰 사용
    path('profile-management/', views.profile_management, name='profile_management'),  # 프로필 관리 페이지
    path('user_problem/', views.user_problem, name='user_problem'),  # 문제 해결 페이지
    path('problem-creation/', views.problem_creation, name='problem_creation'),  # 문제 생성 페이지
    path('question-bank/', views.question_bank, name='question_bank'),  # 문제 은행 페이지
    path('community/', views.community, name='community'),  # 커뮤니티 페이지
    path('blog-post/', views.blog_post, name='blog_post'),  # 블로그 페이지
    path('signup/', views.signup, name='signup'),  # 회원가입 페이지
    path('post/<int:id>/', views.post_detail, name='post_detail'),  # 포스트 상세 페이지
    path('find-id/', views.find_id, name='find_id'),  # ID 찾기 페이지
    path('find-password/', views.find_password, name='find_password'),  # 비밀번호 찾기 페이지
    path('', views.home, name='home'),
    path('profile/', views.profile_management, name='profile_management'),
]