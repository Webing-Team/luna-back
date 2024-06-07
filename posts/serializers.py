from rest_framework import serializers
from .models import Post


class CreatePostSerializer(serializers.ModelSerializer):
    """ Создание поста
    """
    user = serializers.ReadOnlyField(source='user.username')
    title = serializers.CharField()
    text = serializers.CharField()

    class Meta:
        model = Post
        fields = ['user', 'title', 'text']


class ListPostSerializer(serializers.ModelSerializer):
    """ Список постов
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ("id", "user", "text")