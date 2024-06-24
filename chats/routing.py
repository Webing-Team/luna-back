from django.urls import path, re_path

from . import consumers


websocket_urlpatterns = [
    path('ws/chat/<str:chat_slug>/', consumers.ChatConsumer.as_asgi()),
]