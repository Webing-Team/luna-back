import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer
from django.core.paginator import Paginator
from django.contrib.auth.models import AnonymousUser

from .models import Chat, Message
from accounts.models import User
from .serializers import MessageSerializer, ChatSerializer, UserSerializer




class ChatConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = "pk"
    
    async def connect(self):
        await self.channel_layer.group_add(f'chat', self.channel_name)

        try:
            self.user = self.scope.get('user')
            self.chat_id = self.scope['url_route']['kwargs']['id']
            await self.channel_layer.group_add(f'chat-{self.chat_id}', self.channel_name)
            chat_users = await self.get_chat_users()
            if any(u['id'] == self.user.id for u in chat_users):
                print('Accepted')
                await self.accept()
            else:
                await self.close()
        except Exception as e:
            print('Connecting exception:', e)
        
    
            
    
    @database_sync_to_async
    def get_chat_users(self):
        chat = Chat.objects.get(id=self.chat_id)
        return list(chat.current_users.values('id'))    
    
    @sync_to_async
    def get_chat_data(self, page_num: int, **kwargs):
        queryset = Message.objects.filter(chat_id=self.chat_id).order_by('-created_at')
        paginator = Paginator(queryset, 50)
        result = paginator.get_page(page_num)
        messages = []
        for message in result:
            messages.append({
                'message_id': message.id,
                "user_id": message.user.id,
                "text": message.text,
                "created_at": message.created_at.strftime("%d-%m-%Y %H:%M:%S")
            })
        return messages

    async def display_messages(self, event):
        if event['action'] == 'send_message':
            await self.send_json(
                {
                    'action': 'new_message',
                    'message': event['message']    
                }
            )

        
    @action()
    async def load_chat_messages(self,  page_num: int, **kwargs):
        messages = await self.get_chat_data(chat_id=self.chat_id, page_num=page_num, **kwargs)
        print('chat is loading')
        await self.send_json({
            'action': 'load_chat',
            'messages': messages
            })
            
    @action()
    async def send_message(self, message_text: str,  **kwargs):
        message = await database_sync_to_async(Message.objects.create)(user=self.user, chat_id=self.chat_id, text=message_text)
        await self.channel_layer.group_send(
            f'chat-{self.chat_id}',
            {
                'type': 'display_messages',
                'action': 'send_message',
                'message': {
                    'message_id': message.id,
                    "user_id": message.user.id,
                    "text": message.text,
                    "created_at": message.created_at.strftime("%d-%m-%Y %H:%M:%S")
                },
            }
        )

    