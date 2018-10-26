from django.urls import path

from . import views

# reverse 또는 템플릿의 {% url %} 태그에서 사용
app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:post_pk>/comments/create/', views.comment_create, name='comment_create'),
    path('tag_search/', views.tag_search, name="tag_search"),
    path('<int:post_pk>/like-toggle/', views.post_like_toggle, name="post_like_toggle"),
]