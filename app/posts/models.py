import datetime
import re

from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(
        # <AppName>.<ModelName>
        # 'members.User',
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    photo = models.ImageField(
        '사진',
        upload_to='post',
    )

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_posts',
        related_query_name='like_post',
        through='PostLike',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    def like_toggle(self, user):
        now_like = PostLike.objects.get_or_create(post=self, user=user)
        if not now_like[1]:
            # 만약 created=True이면 해당 객체 삭제
            now_like[0].delete()


class Comment(models.Model):
    TAG_PATTERN = re.compile(r'#(\w+)')
    # 내가 다수인쪽에 ForeignKey를 작성해야함
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='포스트',
    )
    author = models.ForeignKey(
        # 'members.User',
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    content = models.TextField('댓글 내용')
    tags = models.ManyToManyField(
        'HashTag',
        blank=True,
        verbose_name='해시태그 목록'
    )
    # Commnet 가 save()에서 호출 될 때, content의 내용으로 이 필드를 자동으로 생성
    _html = models.TextField("태그가 Html화된 댓글 내용", blank=True)

    def save(self, *args, **kwargs):
        def save_html():
            self._html = re.sub(self.TAG_PATTERN, r'<a href="/explore/tags/\1">#\1</a>', self.content)

        def save_tags():
            tags = [HashTag.objects.get_or_create(name=name)[0] for name in re.findall(self.TAG_PATTERN, self.content)]
            self.tags.set(tags)

        save_html()
        super().save(*args, **kwargs)
        save_tags()

    @property
    def html(self):
        # 자신의 content 속성값에서 #문자열 -> <a href="/explore/tags/<문자열>">#문자열</a>

        # /explorer/tags/{태그명}/ URL에서
        # 해당 태그를 가진 POST 목록을 보여주는 view, url, template 구현
        # URL name : tag_post_list
        # view:
        #       tag_post_list(request, tag_name)
        # template:
        #       /posts/tag_post_list.html

        # base.html에 있는 검색창에 값을 입력하고 Enter시 (Submit)
        # 해당 값을 사용해 위에서 만든 view로 이동
        return self._html


    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = f'{verbose_name} 목록'


class HashTag(models.Model):
    name = models.CharField('태그명', max_length=100, unique=True)

    class Meta:
        verbose_name = '해시태그'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name


#1. post_list에서 Like 한 유저 목록을 표시
#       ex ) pby, parkboyoung, lhy 님이 좋아합니다.

class PostLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='포스트',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post'), )