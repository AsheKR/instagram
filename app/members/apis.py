from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.serializers import UserSerializer

User = get_user_model()


class AuthTokenView(APIView):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'Token': token.key})
        else:
            raise AuthenticationFailed


class ProfileView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
