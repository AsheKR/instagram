from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post, Comment, PostLike

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = (
            'author',
            'content',
        )


class PostSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    like_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'author',
            'photo',
            'created_at',
            'like_users',
            'comment_set',
        )
        read_only_fields = (
            'author',
        )
