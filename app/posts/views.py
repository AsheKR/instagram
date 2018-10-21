from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from members.models import User
from .models import Post


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

def post_create(request):
    # 1. form 구현 input[type=file], button[submit]
    # 2. /posts/create/ uRL에 이 view를 연결
    # 3. base.html 의 '+ Add Post' 텍스트를 갖는 a 링크 하나 추가
    #   {% url %} 태그를 사용해 포스트 생성 링크 검
    if request.method == 'POST':
        author = User.objects.get(pk=1)
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save('post/'+photo.name, photo)

        Post.objects.create(author=author, photo=photo)
        return redirect('posts:post-list')
    else:
        return render(request, 'posts/post_create.html')