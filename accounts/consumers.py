from djangochannelsrestframework import mixins
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from datetime import timezone
import json 

from .models import User
from .serializers import UserSerializer

class UserConsumer(
    
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.PatchModelMixin,
        mixins.UpdateModelMixin,
        mixins.CreateModelMixin,
        mixins.DeleteModelMixin,
        GenericAsyncAPIConsumer,
):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # @database_sync_to_async
    @database_sync_to_async
    def update_user_activity(self, is_active: bool):
        self.user.is_online=is_active
        if not is_active:
            self.user.was_online_at=timezone.now()
        self.user.save()
        
    async def connect(self, *args, **kwargs):
        await self.channel_layer.group_add(
            'user_group',
            self.channel_name
        )
        user = self.scope.get('user')
        print(user)
        if user:
            await self.accept()
            if user != AnonymousUser:
                self.user = user
                await self.update_user_activity(is_active=True)
                await self.send(text_data=json.dumps({'message_type': 'user_activity_update',
                                    'user': self.user.id,
                                    'online_status': self.user.is_online,
                                    'was_online_at': "online"}))
            else:
                self.user = None
        else:
            await self.close(reason="User token is not valid.", code=201)
        
        return 1
        
    
    async def disconnect(self, code):
        try:
            if self.user:
                print(self.user)
                await self.update_user_activity(is_active=False)
                await self.send({'message_type': 'user_activity_update',
                                'user': self.user.id,
                                'online_status': self.user.is_online,
                                'was_online_at': self.user.was_online_at})
        except:
            pass
        return await super().disconnect(code)