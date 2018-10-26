from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models

from posts.models import PostLike


class User(AbstractUser):
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='user',
        blank=True,
    )
    site = models.URLField(
        '사이트',
        max_length=150,
        blank=True,
    )
    introduce = models.TextField(
        '소개',
        blank=True,
    )

    def __str__(self):
        return self.username

    def like_post_toggle(self, post_pk):
        now_like = PostLike.objects.get_or_create(post=post_pk, user=self)
        if not now_like[1]:
            # 만약 created=True이면 해당 객체 삭제
            now_like[0].delete()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    @property
    def img_profile_url(self):
        if self.img_profile:
            return self.img_profile.url
        return static('images/user.png')