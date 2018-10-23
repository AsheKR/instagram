from django import forms

from posts.models import Post


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
            **kwargs,
        )
        return post
