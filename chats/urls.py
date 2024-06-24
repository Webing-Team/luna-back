from django.urls import path

from . import views

urlpatterns = [
    # path('test/', views.test), # only for websocket testing
    path('start_chat/', views.CreateChatView.as_view(), name='create_chat')
]