from django.urls import path

from . import views

# reverse 또는 템플릿의 {% url %} 태그에서 사용
app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list')
]