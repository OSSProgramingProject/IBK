# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from .models import UserProfile
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Follow, Friendship, Message, BlogPost, Problem, Question, Data
from .forms import FollowForm, MessageForm, BlogPostForm, ProblemForm, QuestionForm, DataForm
from django.db.models import Q
from django.db import models
from django.core.paginator import Paginator
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
        'solved_problems': user_profile.solved_problems if user_profile else None,
        'friends': Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user)),
        'messages_received': Message.objects.filter(receiver=request.user),
        'messages_sent': Message.objects.filter(sender=request.user),
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

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            receiver_username = form.cleaned_data['receiver']
            content = form.cleaned_data['content']
            
            # Check if the receiver exists
            try:
                receiver = User.objects.get(username=receiver_username)
                # Create the message instance
                Message.objects.create(sender=request.user, receiver=receiver, content=content)
                messages.success(request, 'Message sent successfully.')
            except User.DoesNotExist:
                messages.error(request, 'The specified user does not exist.')
                
            return redirect('profile_management')
    else:
        form = MessageForm()
    
    return render(request, 'profile-management.html', {'form': form})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted successfully.')
        return redirect('profile_management')
    return render(request, 'confirm_delete.html', {'message': message})

@login_required
def add_friend(request):
    if request.method == 'POST':
        friend_username = request.POST.get('friend_username')
        if friend_username:
            friend_user = get_object_or_404(User, username=friend_username)
            if not Friendship.objects.filter(user1=request.user, user2=friend_user).exists():
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
            blog_post = form.save(commit=False)
            blog_post.author = request.user

            # 문제 정보가 있으면 저장
            blog_post.contest_id = request.POST.get('contest_id', '')
            blog_post.index = request.POST.get('index', '')
            blog_post.problem_name = request.POST.get('problem_name', '')
            blog_post.tags = request.POST.get('tags', '')

            blog_post.save()
            return redirect('blog_post')
    else:
        # 문제 풀기 버튼에서 넘어온 문제 정보 가져오기
        contest_id = request.GET.get('contestId', '')
        index = request.GET.get('index', '')
        name = request.GET.get('name', '')
        tags = request.GET.get('tags', '')

        # 문제 정보가 있다면 초기 내용 작성
        initial_content = ""
        if contest_id and index and name:
            initial_content = f"Problem: {contest_id} - {index} ({name})\nTags: {tags}\n\nPlease describe your solution here..."

        # 초기 값을 포함한 폼 생성
        form = BlogPostForm(user=request.user, initial={'content': initial_content})

    return render(request, 'blog_creation.html', {
        'form': form,
        'contest_id': contest_id,
        'index': index,
        'problem_name': name,
        'tags': tags
    })


def blog_post(request):
    # 로그인한 사용자의 게시글과 전체공개 게시글만 가져오기
    if request.user.is_authenticated:
        blog_posts = BlogPost.objects.filter(
            models.Q(visibility='public') | models.Q(author=request.user)
        )
    else:
        blog_posts = BlogPost.objects.filter(visibility='public')
    
    return render(request, 'blog-post.html', {'blog_posts': blog_posts})

def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})

@login_required
def blog_edit(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)

    # 작성자가 아닌 사용자가 접근하려고 할 때
    if blog_post.author != request.user:
        messages.error(request, "You are not authorized to edit this blog post.")
        return redirect('blog_post')

    # POST 요청 시 폼 처리
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post, user=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully.")

            # 수정 후 돌아갈 페이지 결정
            source = request.GET.get('source', 'blog')
            if source == 'user_problem':
                return redirect('user_problem')
            else:
                return redirect('blog_post')

    # GET 요청 시 폼 초기화
    else:
        form = BlogPostForm(instance=blog_post, user=request.user)

    return render(request, 'blog_edit.html', {'form': form, 'blog_post': blog_post})

@login_required
def blog_delete(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)

    # 작성자인지 확인
    if blog_post.author == request.user:
        blog_post.delete()
        messages.success(request, "Blog post deleted successfully.")

        # 삭제 후 돌아갈 페이지 결정
        source = request.GET.get('source', 'blog')
        if source == 'user_problem':
            return redirect('user_problem')
        else:
            return redirect('blog_post')
    else:
        # 작성자가 아닌 경우 접근 거부 처리
        messages.error(request, "You are not authorized to delete this blog post.")
        return redirect('blog_detail', pk=pk)
    
def blog_search(request):
    query = request.GET.get('q')
    blog_posts = BlogPost.objects.filter(title__icontains=query) if query else []
    return render(request, 'blog-post.html', {'blog_posts': blog_posts, 'query': query})


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
            messages.error(request, '회원가입에 실패했습니다. 입력 정보를 다시 확인해주세요.')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'post_detail.html', {'post': post})

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

def findpassword(request):
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
                return redirect('findpassword_result')

            else:
                messages.error(request, '아이디와 이메일이 일치하지 않습니다.')
                return redirect('findpassword')

        except UserProfile.DoesNotExist:
            messages.error(request, '해당 이메일을 사용하는 계정을 찾을 수 없습니다.')
            return redirect('findpassword')

    return render(request, 'findpassword.html')

def find_id_result(request):
    return render(request, 'findid_result.html')

def findpassword_result(request):
    return render(request, 'findpassword_result.html')

def qa_board(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'qa_board.html', {'questions': questions})

def resources_board(request):
    datas = Data.objects.all().order_by('-created_at')
    return render(request, 'resources-board.html', {'datas': datas})


def question_bank(request):
    # API 요청 보내기
    response = requests.get("https://codeforces.com/api/problemset.problems")
    
    if response.status_code == 200:
        # 응답이 성공적이면 데이터를 JSON 형식으로 파싱
        data = response.json()
        problems_list = data.get("result", {}).get("problems", [])
    else:
        # 요청이 실패한 경우 빈 리스트로 설정
        problems_list = []

    # 검색어, 난이도, 태그 가져오기
    search_tags = request.GET.get('tags', '').lower()
    difficulty = request.GET.get('difficulty', '')
    
    if search_tags:
        problems_list = [
            problem for problem in problems_list
            if search_tags in ', '.join(problem.get('tags', [])).lower()
        ]
    
    if difficulty:
        try:
            difficulty = int(difficulty)
            problems_list = [problem for problem in problems_list if problem.get('rating') == difficulty]
        except ValueError:
            pass  # 난이도가 숫자가 아닐 경우, 필터링을 적용하지 않음

    # 페이징 설정
    paginator = Paginator(problems_list, 7)  # 한 페이지에 7개의 문제만 표시
    page_number = request.GET.get('page')
    problems = paginator.get_page(page_number)

    # 템플릿에 데이터를 전달하며 렌더링
    return render(request, 'question-bank.html', {'problems': problems, 'tags': search_tags, 'difficulty': difficulty, 'rating_range': range(100, 4501, 100)})


def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST, request.FILES)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.example_input = form.cleaned_data.get('example_input')
            problem.example_output = form.cleaned_data.get('example_output')
            problem.author = request.user
            problem.save()
            print("문제 저장 완료:")  # 디버깅: 저장된 데이터 확인
            return redirect('user_problem')
        else:
            print("폼 유효성 실패:", form.errors)  # 디버깅: 유효성 실패 이유 출력
    else:
        form = ProblemForm()
    return render(request, 'problem-creation.html', {'form': form})

@login_required
def user_problem(request):
    # 사용자가 작성한 문제 목록 가져오기
    user_problems = Problem.objects.filter(author=request.user)

    # 사용자가 작성한 블로그 게시글 목록 가져오기
    user_blogs = BlogPost.objects.filter(author=request.user)

    # 공개된 마지막 게시글 가져오기 (예시)
    latest_post = BlogPost.objects.filter(visibility='public').last()

    # 템플릿에 전달할 데이터
    context = {
        'user_problems': user_problems,
        'user_blogs': user_blogs,
        'latest_post': latest_post,
    }

    return render(request, 'user_problem.html', context)

@login_required
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    return render(request, 'problem.html', {'problem': problem})


@login_required
def edit_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk, author=request.user)  # 작성자만 수정 가능
    if request.method == 'POST':
        form = ProblemForm(request.POST, request.FILES, instance=problem)
        if form.is_valid():
            form.save()
            messages.success(request, "문제가 성공적으로 수정되었습니다.")
            return redirect('problem_detail', pk=problem.pk)
        else:
            messages.error(request, "문제를 수정하는 데 오류가 발생했습니다.")
    else:
        form = ProblemForm(instance=problem)
    return render(request, 'problem_edit.html', {'form': form, 'problem': problem})


@login_required
def delete_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    # 현재 사용자와 문제 작성자 비교
    if problem.author != request.user:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect('user_problem')

    # 문제 삭제
    problem.delete()
    messages.success(request, "문제가 성공적으로 삭제되었습니다.")
    return redirect('user_problem')

# 질문 생성
@login_required
def qa_creation(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            messages.success(request, '질문이 성공적으로 등록되었습니다.')
            return redirect('qa_board')
    else:
        form = QuestionForm()
    return render(request, 'qa_creation.html', {'form': form})

@login_required
def qa_edit(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if question.author != request.user:
        messages.error(request, "You are not authorized to edit this question.")
        return redirect('qa_board')
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, '질문이 성공적으로 수정되었습니다.')
            return redirect('question_detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'qa_edit.html', {'form': form, 'question': question})

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'question_detail.html', {'question': question})

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.author != request.user:
        return HttpResponseForbidden("삭제할 권한이 없습니다.")
    question.delete()
    return redirect('qa_board')  # 질문 목록 페이지로 리다이렉트


@login_required
def data_upload(request):

    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.author = request.user  # 현재 로그인한 사용자를 작성자로 설정
            data.save()
            messages.success(request, '자료가 성공적으로 업로드되었습니다.')
            return redirect('resources_board')  # 업로드 후 자료 게시판으로 리다이렉트
    else:
        form = DataForm()
    
    return render(request, 'data_upload.html', {'form': form})


@login_required
def data_edit(request, data_id):
    data = get_object_or_404(Data, id=data_id)
    if data.author != request.user:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('resources_board')
    
    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, '자료가 성공적으로 수정되었습니다.')
            return redirect('data_detail', data_id=data.id)
    else:
        form = DataForm(instance=data)
    return render(request, 'data_edit.html', {'form': form, 'data': data})

def data_detail(request, data_id):
    data = get_object_or_404(Data, id=data_id)
    return render(request, 'data_detail.html', {'data': data})

@login_required
def data_delete(request, id):
    data = get_object_or_404(Data, id=id)
    if data.author != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")
    data.delete()
    return redirect('resources_board')
