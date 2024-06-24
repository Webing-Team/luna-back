from asgiref.sync import sync_to_async
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

from rest_framework import generics, serializers, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import User
from .models import User, Chat, Message
from .serializers import ChatSerializer

# function for websocket testing
# def test(request):
#     return render(request, 'chats/test.html', context={"users": User.objects.all()})


class CreateChatView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )
    
    

