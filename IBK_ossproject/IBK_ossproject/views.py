from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile  # Post 모델을 사용한다고 가정
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

# 기존 뷰 함수들
def home(request):
    return render(request, 'home.html')  # home.html을 렌더링

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome, {username}!')
            return redirect('profile_management')  # 로그인 후 프로필 관리 페이지로 이동
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')  # login.html을 렌더링

def user_logout(request):
    auth_logout(request)
    return redirect('home')


@login_required # 이 데코레이터를 사용하면 로그인한 사용자만 특정 페이지에 접근하도록 할 수 있음
def profile_management(request):
    # 현재 사용자를 가져옵니다 (예를 들어, user_id가 1인 사용자라고 가정)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        #user_name = user_profile.user_name # UserProfile 모델의 user_name 속성 접근
    except UserProfile.DoesNotExist:
    # 예외 처리 - 사용자 프로필이 없을 때
        user_profile = None
    
    if request.method == "POST":
        request.user.username = request.POST.get('user_name')
        request.user.save()
        user_profile.solved_problems = request.POST.get('solved_problems')
        user_profile.save()  # 변경 사항 저장

        return redirect('profile_management')

    # 페이지 로드 시 현재 사용자 정보를 컨텍스트로 전달하여 렌더링
    context = {
        'user_profile': user_profile,
        'user_name' : request.user.username,
        # 'user_name': user_profile.user.user_name, # 문제발생지점
        'solved_problems': user_profile.solved_problems,
    }
    return render(request, 'profile-management.html', context)
    
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
        print(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # 사용자 저장
            username = form.cleaned_data.get('username')
            messages.success(request, f'계정이 생성되었습니다. {username}님, 로그인하세요.')
            return redirect('login')  # 회원가입 후 로그인 페이지로 이동
        else:
            # 폼 유효성 검사 실패 시 오류 메시지 출력
            messages.error(request, '회원가입에 실패했습니다. 입력 정보를 다시 확인해주세요.')
            print(form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})

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
