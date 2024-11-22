from django.shortcuts import render, redirect

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
