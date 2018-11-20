from django.urls import path, include

from posts import apis

urlpatterns_api_posts = [
    path('', apis.PostList.as_view(), name='post_list'),
    path('postlike/<int:pk>/', apis.PostLikeDestroyAPIGenericView.as_view()),
    path('<int:pk>/', apis.PostDetail.as_view(), name='post_detail'),
    path('postlike/', apis.PostLikeCreateAPIView.as_view()),
    path('likes/<int:post_pk>/', apis.PostLikeCreateDestroy.as_view(), name='post_like'),
]

urlpatterns = [
    path('tag-search/', apis.tag_search, name='tag_search'),
    path('', include(urlpatterns_api_posts))
]