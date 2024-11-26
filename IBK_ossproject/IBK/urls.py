from django.urls import path
from IBK_ossproject import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os
urlpatterns = [
    path('', views.home, name='home'),  # 홈 페이지
    path('login/', views.user_login, name='login'),  # 로그인 페이지
    path('logout/', views.user_logout, name='logout'), # 로그아웃
    path('profile-management/', views.profile_management, name='profile_management'),  # 프로필 관리 페이지
    path('user_problem/', views.user_problem, name='user_problem'),  # 문제 해결 페이지
    path('problem-creation/', views.problem_creation, name='problem_creation'),  # 문제 생성 페이지
    path('question-bank/', views.question_bank, name='question_bank'),  # 문제 은행 페이지
    path('community/', views.community, name='community'),  # 커뮤니티 페이지
    path('blog-post/', views.blog_post, name='blog_post'),  # 블로그 페이지
    path('signup/', views.signup, name='signup'),  # 회원가입 페이지
    path('post/<int:id>/', views.post_detail, name='post_detail'),  # 포스트 상세 페이지
    path('find-id/', views.find_id, name='find_id'),  # ID 찾기 페이지
    path('find-id-result/', views.find_id_result, name='findid_result'),  # 아이디 찾기 결과
    path('findpassword/', views.findpassword, name='findpassword'),  # 비밀번호 찾기 페이지
    path('findpassword-result/', views.findpassword_result, name='findpassword_result'),  # 비밀번호 찾기 결과 페이지
    path('profile/', views.profile_management, name='profile_management'),  # 프로필 관리 페이지
    path('admin/', admin.site.urls), #관리자 페이지 경로 설정
    
]
if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])