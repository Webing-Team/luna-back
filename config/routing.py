from django.urls import path, re_path, include

from accounts import consumers as user_consumers
from chats import consumers as chat_consumers


websocket_urlpatterns = [
    path("ws/user-ws/", user_consumers.UserConsumer.as_asgi(), name='user-websocket'),
    path('ws/chat/<int:id>/', chat_consumers.ChatConsumer.as_asgi()),
]