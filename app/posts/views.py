from django.shortcuts import render

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