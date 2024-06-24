from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Group
from .serializers import CreateGroupSerializer, CreateGroupPostSerializer, JoinGroupSerializer



class CreateGroupView(generics.CreateAPIView):
    """ Create group
    """
    serializer_class = CreateGroupSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)

            return Response({
                'status': 'success',
                'detail': 'The group was successfully created.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user.id)
    

class CreatePostView(generics.CreateAPIView):
    """ Create new post 
    """
    serializer_class = CreateGroupPostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        group_id = self.kwargs['group_id']
        group = Group.objects.get(id=group_id)
        if group.users.filter(user=self.request.user).exists():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({
                'status': 'success',
                'detail': 'Post successfully created',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'error',
                'detail': 'You are not a member of this group'
            }, status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        group_id = self.kwargs['group_id']
        group = Group.objects.get(id=group_id)
        serializer.save(user=self.request.user.profile, group=group)


class DeleteGroupView(generics.DestroyAPIView):
    """ Delete group
    """
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def delete(self, request):
        instance = get_object_or_404(Group, admins=self.request.user.profile)
        instance.delete()
        return Response({
            'status': 'success',
            'detail': 'group deleted successfully'
        }, status=status.HTTP_200_OK)


class JoinGroupView(generics.RetrieveAPIView):
    """ Joining a group
    """
    queryset = Group.objects.all()
    serializer_class = JoinGroupSerializer
    lookup_field = 'id'
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def retrieve(self, request, *args, **kwargs):
        group = self.get_object()
        user = self.request.user.profile

        if group.users.filter(user_id=user.id).exists():
            return Response({
                'status': 'error',
                'detail': 'you are already a member of the group'
            }, status=status.HTTP_400_BAD_REQUEST)

        group.users.add(user)
        group.save()
        
        return Response({
            'status': 'success',
            'detail': 'you have joined the group',
        }, status=status.HTTP_202_ACCEPTED)