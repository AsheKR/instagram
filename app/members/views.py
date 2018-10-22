from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm


# Create your views here.
def login_view(request):
    # URL: /members/login/
    # config.urls에서 '/memebers/' 부분을 include
    # members.url에서 '/login/' 부분을 이 view에 연결

    # Template: members/login.html
    # 템플릿에는 GET 요청시 아래의 LoginForm 인스턴스를 사용
    # POST 요청시의 처리는 아직 하지 않음

    # Form: members/forms.py
    #   class LoginForm
    #       username, password를 받을 수 있도록 함
    #       paswords는 PasswordInput 위젯을 사용
    if request.method == 'POST':
        # 1. reqiest.POST에 데이터가 옴
        # 2. 온 데이터 중에서 username 해당하는 값과 password에 해당하는 값을 각각 변수에 할당
        # 3. 사용자 인증을 수행
        # 4. 인증에 성공하면 세션/쿠키 기반의 로그인 과정을 수행, 완료 후 posts:post_list 페이지로 리다이렉트
        # 5. 인증에 실패하면 이 페이지에서 인증에 실패했음을 사용자에게 알림
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts:post_list')
        else:
            form = LoginForm(request.POST)
            context = {
                'form': form,
                'error': "가입 된 사람이 없습니다."
            }
            return render(request, 'members/login.html', context)

    else:
        form = LoginForm()
        context = {
            'form': form
        }

        return render(request, 'members/login.html', context)


def logout_view(request):
    # URL: /members/logout/
    # Template: 없음

    # !POST 요청일 때만 처리
    # 처리 완료 후 'posts:post_list'로 이동

    # base.html에 있는 'Logout' 버튼이 이 view로 POST 요청하도록 함
        # -> form을 구현해야함
            # 'action' 속성의 값을 이 view로
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post_list')


def signup_view(request):
    # URL: /members/signup/
    # Template: members/signup.html
    # Form:
    # SignupForm
    # username, password1, password2
    # 나머지 요소들은 login.html의 요소를 최대한 재활용
    if request.method == "POST":
        # 1. request.POST에 전달된 username, password1, password2를 각각 해당 이름의 변수에 할당
        # 2-1. username에 해당한 User가 이미 있다면 사용자명 {{ username }} 은 이미 사용중입니다.
        # 2-2. password1과 password2가 일치하지 않는다면 비밀번호와 비밀번호 확인란의 값이 일치하지 않습니다.
        # 3. 위 두경우 모두 아니면 새 User 객체 생성, 로그인 후 'posts:post_list'로 리다이렉트 처리
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        form = SignupForm(request.POST)
        context = {
            'form': form,
        }

        if User.objects.filter(username=username).exists():
            context['error'] = username + "은 이미 사용중 입니다."
        elif password1 != password2:
            context['error'] = "패스워드 값이 일치하지 않습니다."
        else:
            # create_user 를 사용하여야 정상적인 로그인이 가능하다.
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect('posts:post_list')
        return render(request, 'members/signup.html', context)



    else:
        form = SignupForm()
        context = {
            'form': form
        }
        return render(request, 'members/signup.html', context)
