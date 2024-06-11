from rest_framework import generics, status
from .models import Post
from .serializers import ListPostSerializer, CreatePostSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response


class CreatePostView(generics.CreateAPIView):
    """ Создание нового поста """
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostListView(generics.ListAPIView):
    """Список постов на стене пользователя"""
    serializer_class = ListPostSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        return Post.objects.filter(user_id=user_id)
