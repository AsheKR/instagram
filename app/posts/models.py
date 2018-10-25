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

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        content = self.content
        tags = [HashTag.objects.get_or_create(name=name)[0] for name in re.findall(self.TAG_PATTERN, self.content)]
        self.tags.set(tags)

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
        return re.sub(r'#(\w+)', r'<a href="/explore/tags/\1">#\1</a>', self.content)


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
