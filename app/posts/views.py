import re

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

# from members.models import User
from .models import Post, Comment, HashTag
from .forms import PostCreateForm, CommentCreateForm, CommentForm, PostForm


def post_list(request):
    # 1. created_at, modified_at 필드를 추가
    # 2. Post 모델이 기본적으로 pk 내림차순으로 정렬되도록 설정
    # 3. 모든 Post객체에 대한 QuerySet을 render의 context 인수를 전달 (키: posts)
    # 4. posts/post_list.html 을 Template로 사용, 각 템플릿에서는 post 값을 순회하며 각 Post의 Photo를 출력
    # 5. url은 posts.urls 모듈을 사용. config.urls에서 해당 모듈을 include
    #       posts/ 로 접근시 이 view 가 처리

    posts = Post.objects.all()
    comment_form = CommentForm()

    context = {
        'comment_form': comment_form,
        'posts': posts,

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
        #           ModelForm
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            comment_content = form.cleaned_data['comment']

            if comment_content:
                post.comment_set.create(
                    author=request.user,
                    content=form.cleaned_data['comment'],
                )
            return redirect('posts:post_list')


        #           PostCreateForm
        # form = PostCreateForm(request.POST, request.FILES)
        # if form.is_valid():
        #     form.save(author=request.user)
        #     return redirect('posts:post_list')
    else:
        # GET 요청의 경우, 빈 Form인스턴ㅅ트를 context에 담아 전달
        # Tempatle에는 `form` 키로 해당 Form 인스턴스 속성을 사용 가능
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/post_create.html', context)


def comment_create(request, post_pk):
    """
    post_pk에 해당하는 Post에 댓글을 생성하는 view
    'POST'메서드 요청만 처리

    'content' 키로 들어온 값을 사용해 댓글 생성. 작성자는 요청한 User
    URL: /posts/<post_pk>/comments/create/

    댓글 생성 완료 후에는 posts:post-list로 리다이렉트

    :param request:
    :param post_pk:
    :return:
    """

    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            # Comment가 가진 content 속성에서 해시태그에 해당하는 문자열을 가져와서
            # 해시태그에 해당하는 문자열을 가져와서
            # HashTag객체를 가져오거나 생성(get_or_create)
            # 이후 comment.tags에 해당 객체들을 추가
            #       이 내용은 모델의 Save() 메서드로 옮김
            # content = comment.content
            # tags = [HashTag.objects.get_or_create(name=name)[0] for name in re.findall(r'#(\w+)', content)]
            # comment.tags.set(tags)

            # hashtag_list = re.findall(r'#(\w+)', content)
            # for hashtag in hashtag_list:
            #     tag = HashTag.objects.get_or_create(name=hashtag)
            #     if tag[1]:
            #         comment.tags.add(tag[0])

            return redirect('posts:post_list')

        # content = request.POST['content']
        # Comment.objects.create(content=content, author=request.user, post=post)
        # return redirect('posts:post_list')