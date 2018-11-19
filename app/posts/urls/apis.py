from django.urls import path

from posts import apis

urlpatterns = [
    path('tag-search/', apis.tag_search, name='tag_search'),
    path('', apis.PostList.as_view(), name='post_list'),
    path('<pk>/', apis.PostDetail.as_view(), name='post_detail'),
    path('likes/<int:post_pk>/', apis.PostLikeCreate.as_view(), name='post_like'),
]