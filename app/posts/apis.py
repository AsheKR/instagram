import json

from django.http import HttpResponse, Http404
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, HashTag
from posts.serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(APIView):
    # URL: /api/posts/<pk>/
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_objects(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_objects(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None, **kwargs):
        post = self.get_objects(pk)
        serializer = PostSerializer(post, data=request.data, **kwargs)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def pacth(self, request, pk, format=None):
        self.put(request, pk, format, partial=True)

    def delete(self, request, pk, format=None):
        post = self.get_objects(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 페이지를 리턴하지 않고 데이터를 리턴하기 때문에 view가 아닌 apis에 사용
def tag_search(request):
    search_keyword = request.GET.get('keyword', 'sun')
    if search_keyword:
        tags = list(HashTag.objects.filter(name__istartswith=search_keyword).values())
    result = json.dumps(tags)
    return HttpResponse(result, content_type='application/json')
