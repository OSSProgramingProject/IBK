from django.shortcuts import render, redirect, get_object_or_404
from .models import Post  # Post 모델을 사용한다고 가정

# 기존 뷰 함수들
def home(request):
    return render(request, 'home.html')  # home.html을 렌더링

def login(request):
    return render(request, 'login.html')  # login.html을 렌더링

def profile_management(request):
    return render(request, 'profile-management.html')  # profile-management.html을 렌더링

def user_problem(request):
    return render(request, 'user_problem.html')  # user-problem.html을 렌더링

def problem_creation(request):
    return render(request, 'problem-creation.html')  # problem-creation.html을 렌더링

def question_bank(request):
    return render(request, 'question-bank.html')  # question-bank.html을 렌더링

def community(request):
    return render(request, 'community.html')  # community.html을 렌더링

def blog_post(request):
    return render(request, 'blog-post.html')  # blog-post.html을 렌더링

# 새로 추가된 signup 뷰 함수
def signup(request):
    if request.method == 'POST':
        # POST 요청 시 회원가입 처리 로직 (예시)
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # 여기서 사용자를 생성하거나 이메일 확인 등의 로직을 추가합니다
        # 예시로 사용자 생성만 처리
        # User.objects.create_user(username=username, password=password, email=email)
        
        return redirect('login')  # 회원가입 후 로그인 페이지로 리다이렉트

    return render(request, 'signup.html')  # GET 요청 시 signup.html을 렌더링

# 새로운 포스트 상세 뷰 함수
def post_detail(request, id):
    # id에 해당하는 포스트를 가져옵니다. 해당 포스트가 없으면 404 에러를 반환합니다.
    post = get_object_or_404(Post, id=id)
    
    # 'post_detail.html' 템플릿에 해당 포스트 데이터를 전달
    return render(request, 'post_detail.html', {'post': post})


# ID 찾기 뷰 함수
def find_id(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # 이메일로 사용자 ID 검색 로직 추가
        # 예: user = User.objects.filter(email=email).first()
        # 예: user_id = user.username if user else None
        
        user_id = "example_id"  # 실제 로직 구현 후 대체
        return render(request, 'findid_result.html', {'user_id': user_id})
    
    return render(request, 'findid.html')  # GET 요청 시 findid.html 렌더링

# 비밀번호 찾기 뷰 함수
def find_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # 이메일로 비밀번호 찾기 로직 추가 (보안상 임시 비밀번호 발급 추천)
        # 예: user = User.objects.filter(email=email).first()
        # 예: 발급된 임시 비밀번호 이메일 전송 로직 추가
        
        success = True  # 실제 로직 구현 후 성공 여부 반환
        return render(request, 'findpassword_result.html', {'success': success})
    
    return render(request, 'findpassword.html')  # GET 요청 시 findpassword.html 렌더링
