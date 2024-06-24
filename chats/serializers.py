from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer
from .models import Chat, Message

class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Message
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj: Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")


class ChatSerializer(serializers.ModelSerializer):
    # last_message = serializers.SerializerMethodField()
    current_users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    

    class Meta:
        model = Chat
        fields = ['id', 'current_users']
        # depth = 1
        # read_only_fields = ["last_message"]

    # def get_last_message(self, obj: Chat):
    #     return MessageSerializer(obj.messages.order_by('created_at').last()).data