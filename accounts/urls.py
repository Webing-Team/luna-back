from django.urls import path

from .views import CreateUserView, LoginUserView, UserDetailView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('user/<str:token>/', UserDetailView.as_view(), name='user-detail'),
]