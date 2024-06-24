from django.urls import path

from .views import CreateGroupView, JoinGroupView, DeleteGroupView, CreatePostView


urlpatterns = [
    path('create/', CreateGroupView.as_view(), name='create_group'),
    path('delete/', DeleteGroupView.as_view(), name='delete_group'),
    path('join/<int:id>/', JoinGroupView.as_view(), name='join_group'),
    path('create-post/<int:group_id>/', CreatePostView.as_view(), name='create_post')
]