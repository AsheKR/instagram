import json

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm, DivErrorList, UserProfileForm


# Create your views here.
def login_view(request):
    # URL: /members/login/
    # config.urls에서 '/memebers/' 부분을 include
    # members.url에서 '/login/' 부분을 이 view에 연결
    #
    # Template: members/login.html
    # 템플릿에는 GET 요청시 아래의 LoginForm 인스턴스를 사용
    # POST 요청시의 처리는 아직 하지 않음
    #
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
        form = LoginForm(request.POST)

        if form.is_valid():
            login(request, form.user)

            if request.GET.get('next'):
                return redirect(request.GET['next'])
            return redirect('posts:post_list')

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
    context = {}
    if request.method == "POST":
        # POST로 전달된 데이터를 확인
        # 올바르다면 user를 생성하고 post_list 화면으로 이동
        form = SignupForm(request.POST, error_class=DivErrorList)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:post_list')

        # GET요청시 또는 POST 요청 데이터가 올바르지 않을경우
        # 빈 Form 또는 올바르지 않은 데이터에 대한 정보가 포함된 Form을 전달해서
        # 동적으로 form을 렌더링
    else:
        form = SignupForm()

    context['form'] = form
    return render(request, 'members/signup.html', context)


@login_required
def profile(request):
    #  GET요청시 로그인한 유저의 값을 가진 form 을 보여줌

    # POST 요청시 현재 로그인한 유저의 값을 POST 요청에 담겨온 값을 사용해 수정

    context = {}

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                '프로필 수정이 완료되었습니다.'
            )
    form = UserProfileForm(instance=request.user)
    context['form'] = form
    return render(request, 'members/profile.html', context)


def facebook_login(request):
    # URL: /members/facebook_login/
    # URL nmae: 'members:facebook_login'
    # request.GET에 전달된 'code'값을
    # 그대로 HttpResponse로 출력

    api_get_access_token = 'https://graph.facebook.com/v3.2/oauth/access_token'

    # requestToken
    code = request.GET.get('code')
    client_id = '346981992539109'
    redirect_uri = 'http://localhost:8000/members/facebook_login'
    client_secret = '147299406e7de0101fd812189742fe67'

    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'client_secret': client_secret,
        'code': code
    }

    # requestToken to AccessToken
    response = requests.get(api_get_access_token, params)

    # Json To Python Object
    # response_object = json.loads(response.text)
    data = response.json()
    access_token = data.get('access_token')

    # AccessToken을 사용하여 사용자정보 가져오기

    return
