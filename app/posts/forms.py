from django import forms

from posts.models import Post, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            )
        }


class CommentCreateForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '3',
            }
        ),
        label='',
        required=True,
    )

    def save(self, **kwargs):
        comment = Comment.objects.create(
            content=self.cleaned_data['content'],
            **kwargs
        )

        return comment


class PostCreateForm(forms.Form):
    photo = forms.ImageField(
        widget=forms.FileInput(
            # HTML 위젯 속성 설정
            attrs={
                'class': 'custom-file-input'
            }
        )
    )
    comment = forms.CharField(
        # 폼이 반드시 채워져 있을 필요는 없음
        required=False,
        # HTML 렌더링 위젯으로 teatarea 사용
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '3',
            }
        ),
    )

    def save(self, **kwargs):
        post = Post.objects.create(
            photo=self.cleaned_data['photo'],
            author=kwargs.get('author'),
        )

        # 1. POST 생성시 Comment 생성 (선택적)
        # 만약 comment 항목이 있다면
        # 생성한 Post에 연결되는 Comment를 생성
        # author=request.user
        # post=post 가 되도록

        # 2. post_list에서 각 Post 의 댓글 목록 출력

        if self.cleaned_data.get('comment'):
            post.comment_set.create(
                author=kwargs.get('author'),
                content=self.cleaned_data.get('comment')
            )

        return post
