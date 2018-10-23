from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

# from members.models import User
from .models import Post
from .forms import PostCreateForm


def post_list(request):
    # 1. created_at, modified_at 필드를 추가
    # 2. Post 모델이 기본적으로 pk 내림차순으로 정렬되도록 설정
    # 3. 모든 Post객체에 대한 QuerySet을 render의 context 인수를 전달 (키: posts)
    # 4. posts/post_list.html 을 Template로 사용, 각 템플릿에서는 post 값을 순회하며 각 Post의 Photo를 출력
    # 5. url은 posts.urls 모듈을 사용. config.urls에서 해당 모듈을 include
    #       posts/ 로 접근시 이 view 가 처리

    posts = Post.objects.all()

    context = {
        'posts': posts
    }

    return render(request, 'posts/post_list.html', context)


@login_required
def post_create(request):
    # 해당 뷰로 왔는데
    # User가 로그인 된 상태가 아니라면
    # post:post_list로 보내기

    # Django의 Decorator를 사용해서 로그인 체크 기능을 만들어줄 수 있다.
    # if not request.user.is_authenticated:
    #     return redirect('members:login')

    # 1. form 구현 input[type=file], button[submit]
    # 2. /posts/create/ uRL에 이 view를 연결
    # 3. base.html 의 '+ Add Post' 텍스트를 갖는 a 링크 하나 추가
    #   {% url %} 태그를 사용해 포스트 생성 링크 검
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(author=request.user)
            return redirect('posts:post_list')
    else:
        # GET 요청의 경우, 빈 Form인스턴ㅅ트를 context에 담아 전달
        # Tempatle에는 `form` 키로 해당 Form 인스턴스 속성을 사용 가능
        form = PostCreateForm()
    context = {
        'form': form
    }
    return render(request, 'posts/post_create.html', context)