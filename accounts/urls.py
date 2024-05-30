from django.urls import path

from .views import CreateUserView, LoginUserView, UserDataView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('user/<str:token>/', UserDataView.as_view(), name='user-data' ),
]
