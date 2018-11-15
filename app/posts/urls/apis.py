from django.urls import path

from posts import apis

app_name = 'api_posts'

urlpatterns = [
    path('tag-search/', apis.tag_search, name='api_tag_search'),
    path('posts/', apis.PostList.as_view()),
    path('posts/<pk>/', apis.PostDetail.as_view()),
]