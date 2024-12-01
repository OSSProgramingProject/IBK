from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 홈 페이지
    path('login/', views.user_login, name='login'),  # 로그인 페이지
    path('logout/', views.user_logout, name='logout'),  # 로그아웃 페이지
    path('signup/', views.signup, name='signup'),  # 회원가입 페이지

    # 프로필 관리 페이지
    path('profile/', views.profile_management, name='profile_management'),

    # 문제 관련 페이지
    path('user-problem/', views.user_problem, name='user_problem'),  # 문제 해결 페이지
    path('problem/create/', views.problem_creation, name='problem_creation'),  # 문제 생성 페이지
    path('question-bank/', views.question_bank, name='question_bank'),  # 문제 은행 페이지

    # 커뮤니티 및 블로그 관련 페이지
    path('community/', views.community, name='community'),  # 커뮤니티 페이지
    path('blog/', views.blog_post, name='blog_post'),  # 블로그 페이지
    path('blog/<int:id>/', views.post_detail, name='post_detail'),  # 포스트 상세 페이지

    # ID 및 비밀번호 찾기 페이지
    path('find-id/', views.find_id, name='find_id'),  # ID 찾기 페이지
    path('find-id-result/', views.find_id_result, name='find_id_result'),  # 아이디 찾기 결과 페이지
    path('find-password/', views.findpassword, name='find_password'),  # 비밀번호 찾기 페이지
    path('find-password-result/', views.findpassword_result, name='find_password_result'),  # 비밀번호 찾기 결과 페이지

    # Q&A 및 자료 게시판
    path('qa-board/', views.qa_board, name='qa_board'),  # QnA 게시판
    path('resources-board/', views.resources_board, name='resources_board'),  # 자료 게시판
    path('data/upload/', views.data_upload, name='data_upload'),  # 자료 업로드
    path('data/<int:data_id>/', views.data_detail, name='data_detail'),  # 자료 상세 보기
    path('data/<int:data_id>/edit/', views.data_edit, name='data_edit'),  # 자료 수정
    path('qa/<int:question_id>/', views.question_detail, name='question_detail'),  # 질문 상세 페이지
    path('qa/<int:question_id>/edit/', views.qa_edit, name='qa_edit'),  # 질문 수정 페이지 추가



    # 친구 추가 기능
    path('add-friend/', views.add_friend, name='add_friend'),
]
