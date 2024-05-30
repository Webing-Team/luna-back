from django.urls import path

from .views import CreateUserView, LoginUserView, UserView

urlpatterns = [
    path('register', CreateUserView.as_view(), name='create_user'),
    path('login', LoginUserView.as_view(), name='login'),
    path('user/<str:auth_token>', UserView.as_view(), name='get_user'),
    path('user/update/<str:auth_token>', UserView.as_view(), name='update_user', methods=['PUT']),
    path('user/delete/<str:auth_token>', UserView.as_view(), name='delete_user', methods=['DELETE'])
    
]
