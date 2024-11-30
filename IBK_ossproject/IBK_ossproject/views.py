# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Follow, Friendship, Message
from .forms import FollowForm, MessageForm
from django.db.models import Q
from .models import BlogPost
from .forms import BlogPostForm
import requests
import random
import string

# 기존 뷰 함수들
def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def user_logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def profile_management(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    if request.method == "POST":
        request.user.username = request.POST.get('user_name')
        request.user.save()
        user_profile.solved_problems = request.POST.get('solved_problems')
        user_profile.save()

        return redirect('profile_management')

    context = {
        'user_profile': user_profile,
        'user_name': request.user.username,
        'solved_problems': user_profile.solved_problems,
        'friends': Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user)),
    }
    return render(request, 'profile-management.html', context)

def follow_user(request):
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            user_to_follow = get_object_or_404(User, username=form.cleaned_data['user_to_follow'])
            Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
            return redirect('profile_management')
    return redirect('profile_management')

def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            receiver = get_object_or_404(User, username=form.cleaned_data['receiver'])
            content = form.cleaned_data['content']
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            return redirect('profile_management')
    return redirect('profile_management')

@login_required
def add_friend(request):
    if request.method == 'POST':
        friend_username = request.POST.get('friend_username')
        if friend_username:
            friend_user = get_object_or_404(User, username=friend_username)
            # 이미 친구 관계가 있는지 확인
            if not Friendship.objects.filter(user1=request.user, user2=friend_user).exists():
                # 친구 관계 생성
                Friendship.objects.create(user1=request.user, user2=friend_user)
                messages.success(request, f'{friend_user.username}님과 친구가 되었습니다.')
            else:
                messages.info(request, '이미 친구 관계입니다.')
        else:
            messages.error(request, '잘못된 사용자 이름입니다.')

    return redirect('profile_management')

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog_post')
    else:
        form = BlogPostForm(user=request.user)

    return render(request, 'blog_create.html', {'form': form})


def blog_post(request):
    blog_posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog-post.html', {'blog_posts': blog_posts})

def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})

@login_required
def blog_edit(request, pk):
    # 블로그 게시글 가져오기
    blog_post = get_object_or_404(BlogPost, pk=pk)

    # 현재 사용자가 게시글 작성자인지 확인
    if blog_post.author != request.user:
        messages.error(request, "You are not authorized to edit this blog post.")
        return redirect('blog_post')  # 사용자에게 권한이 없을 경우 게시글 목록으로 리디렉션

    # 폼 생성
    if request.method == 'POST':
        # POST 요청 시 폼을 작성하고 유효성을 검사합니다.
        form = BlogPostForm(request.POST, instance=blog_post, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully.")
            return redirect('blog_detail', pk=blog_post.pk)
    else:
        # GET 요청 시 작성된 내용이 미리 채워진 폼을 표시합니다.
        form = BlogPostForm(instance=blog_post, user=request.user)

    # 폼을 렌더링합니다.
    return render(request, 'IBK_ossproject/blog_edit.html', {'form': form, 'blog_post': blog_post})

def user_problem(request):
    return render(request, 'user_problem.html')

def problem_creation(request):
    return render(request, 'problem-creation.html')

def question_bank(request):
    return render(request, 'question-bank.html')

def community(request):
    return render(request, 'community.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() 
            username = form.cleaned_data.get('username')
            messages.success(request, f'계정이 생성되었습니다. {username}님, 로그인하세요.')
            return redirect('login')
        else:
            print(form.errors)
            messages.error(request, '회원가입에 실패했습니다. 입력 정보를 다시 확인해주세요.')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'post_detail.html', {'post': post})

def blog_search(request):
    query = request.GET.get('q')
    blog_posts = BlogPost.objects.filter(title__icontains=query) if query else []

    return render(request, 'blog-post.html', {'blog_posts': blog_posts, 'query': query})

def find_id(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_profile = UserProfile.objects.filter(user__email=email).first()

        if user_profile:
            user_id = user_profile.user.username
            return render(request, 'findid_result.html', {'user_id': user_id})
        else:
            messages.error(request, '해당 이메일을 사용하는 계정을 찾을 수 없습니다.')
            return redirect('find_id')
    
    return render(request, 'findid.html')

def generate_temp_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def findpassword(request):  # 변경된 함수 이름
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')

        try:
            user_profile = UserProfile.objects.get(user__email=email)
            user = user_profile.user

            if user.username == username:
                temp_password = generate_temp_password()
                user.set_password(temp_password)
                user.save()

                subject = '비밀번호 찾기 - 임시 비밀번호'
                message = f'안녕하세요, {user.username}님. 임시 비밀번호는 {temp_password} 입니다. 로그인 후 비밀번호를 변경해주세요.'
                from_email = 'your_real_email@domain.com'
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list)

                messages.success(request, '임시 비밀번호가 이메일로 전송되었습니다.')
                return redirect('findpassword_result')  # 수정된 URL 이름으로 변경

            else:
                messages.error(request, '아이디와 이메일이 일치하지 않습니다.')
                return redirect('findpassword')  # 수정된 URL 이름으로 변경

        except UserProfile.DoesNotExist:
            messages.error(request, '해당 이메일을 사용하는 계정을 찾을 수 없습니다.')
            return redirect('findpassword')  # 수정된 URL 이름으로 변경

    return render(request, 'findpassword.html')  # 수정된 템플릿 파일명

def find_id_result(request):
    return render(request, 'findid_result.html')

def findpassword_result(request):  # 변경된 함수 이름
    return render(request, 'findpassword_result.html')

def leetcode_question_bank(request):
    url = "https://leetcode.com/graphql/"
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com",
    }

    query = """
    {
        problemsetQuestionList(
            categorySlug: ""
            limit: 10
            skip: 0
            filters: {}
        ) {
            total
            questions {
                title
                titleSlug
                difficulty
                topicTags {
                    name
                }
            }
        }
    }
    """
    
    response = requests.post(url, json={"query": query}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        problems = data.get("data", {}).get("problemsetQuestionList", {}).get("questions", [])
    else:
        problems = []

    # 템플릿으로 문제 데이터를 전달
    return render(request, 'leetcode-question-bank.html', {'problems': problems})