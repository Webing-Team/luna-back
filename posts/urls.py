from django.urls import path
from . import views

from .views import CreatePostView, PostListView

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create_post'),
    path('<int:pk>/', PostListView.as_view(), name='user_posts'),
]