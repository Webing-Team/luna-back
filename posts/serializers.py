from rest_framework import serializers
from .models import Post
from accounts.models import User


class CreatePostSerializer(serializers.ModelSerializer):
    """ Create post
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['user', 'title', 'text']


class PostSerializer(serializers.ModelSerializer):
    """ Serializer for user post
    """
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'text')


class PostListSerializer(serializers.ModelSerializer):
    """ Get user posts list through enclosed serializer
    """
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'posts')