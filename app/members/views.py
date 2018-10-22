from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import LoginForm

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
                'form': form
            }
            return render(request, 'members/login.html', context)

    else:
        form = LoginForm()
        context = {
            'form': form
        }

        return render(request, 'members/login.html', context)