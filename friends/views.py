from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import Profile
from .models import FriendShip


class SendFriendRequestView(generics.CreateAPIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request, user_id):
        sender = request.user.profile
        receiver = get_object_or_404(Profile, user_id=user_id)

        if sender == receiver:
            return Response({'error': 'You cant send a friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        if receiver in sender.friends.all():
            return Response({'error': 'Friendship already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        sender.subscribe.add(receiver)
        receiver.subscribers.add(sender)

        return Response({'message': 'Friend request sent successfully.'}, status=status.HTTP_200_OK)


class AcceptFriendRequestView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        receiver = request.user.profile
        sender = get_object_or_404(Profile, user_id=user_id)

        instance = get_object_or_404(FriendShip, from_user=request.user.profile.id, to_user=receiver.id)

        if sender not in receiver.subscribe.all():
            return Response({'error': 'Friend request does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


        sender.subscribe.remove(receiver)
        receiver.subscribers.remove(sender)
        sender.friends.add(receiver)

        instance.delete()

        return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)


class RejectFriendRequestView(APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )
        
    def get(self, request, user_id):
        receiver = request.user.profile
        sender = get_object_or_404(Profile, user_id=user_id)

        instance = get_object_or_404(FriendShip, sender=request.user.profile.id, receiver=receiver.id)

        if sender not in receiver.subscribe.all():
            return Response({'error': 'Friend request does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()

        return Response({'message': 'Friend request rejected.'}, status=status.HTTP_200_OK)