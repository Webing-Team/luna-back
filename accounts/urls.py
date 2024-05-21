from django.urls import path

from .views import CreateUserView, LoginUserView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginUserView.as_view(), name='login'),
]
