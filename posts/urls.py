from django.urls import path

from .views import CreatePostView, PostListView, PostView


urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create_post'),
    path('<int:id>/', PostListView.as_view(), name='user_posts'),
    path('post/<int:post_id>', PostView.as_view(), name='specific_post')
]