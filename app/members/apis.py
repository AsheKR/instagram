from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions, status, generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.serializers import UserSerializer, AuthTokenSerializer

User = get_user_model()


class AuthTokenView(APIView):
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        if self.request.user.pk:
            return get_object_or_404(User, pk=self.request.user.pk)
        else:
            super().get_object()
