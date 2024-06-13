from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from .models import Post
from accounts.models import User
from .serializers import PostListSerializer, CreatePostSerializer, PostSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response


class CreatePostView(generics.CreateAPIView):
    """ Create new post 
    """
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostListView(generics.RetrieveAPIView):
    """ Get list of user posts
    """
    serializer_class = PostListSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    


class PostView(generics.RetrieveAPIView):
    """ Get single post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'