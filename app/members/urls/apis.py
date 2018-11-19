from django.urls import path

from members import apis

app_name = 'api_members'

urlpatterns = [
    path('get_user_token/', apis.AuthTokenView.as_view()),
    path('profile/', apis.ProfileView.as_view()),
]