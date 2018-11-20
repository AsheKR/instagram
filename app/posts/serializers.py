from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
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


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = PostLike
        fields = (
            'pk',
            'user',
            'post',
        )
        read_only_fields = (
            'user',
        )


class PostSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    like_users = UserSerializer(many=True, read_only=True)
    is_like = serializers.SerializerMethodField()

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                post_like = obj.postlike_set.get(user=user)
                return PostLikeSerializer(post_like).data
            except PostLike.DoesNotExist:
                return

    class Meta:
        model = Post
        fields = (
            'author',
            'photo',
            'created_at',
            'like_users',
            'comment_set',
            'is_like',
        )
        read_only_fields = (
            'author',
        )


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs['username'], password=attrs['password'])
        if not self.user:
            raise serializers.ValidationError('유저 정보가 잘못되었다.')
        return attrs

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        return {
            'token': token.key,
            'user': UserSerializer(self.user).data
        }