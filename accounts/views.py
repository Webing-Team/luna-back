from rest_framework.response import Response
from rest_framework import generics, serializers, status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .serializers import CreateUserSerializer, LoginUserSerializer
from .models import User


# function for manage error details
def error_detail(e):
    errors = e.detail
    
    error_messages = []
    for field, messages in errors.items():
        error_messages.append(f'{field}: {messages[0].__str__()}')
    
    return error_messages


# registration view
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                data = serializer.validate(data=request.data)
                user = User.objects.create_user(**data)
                token = Token.objects.create(user=user)
                return Response({
                        'status': 'success',
                        'detail': "User created successfully!",
                        "user": {
                            'email': user.email,
                            'username': user.username,
                        },
                        "token": token.key
                    })

        except serializers.ValidationError as e:
            data = {
                'status': 'error',
                'detail': error_detail(e)
                }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        

# login view 
class LoginUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = LoginUserSerializer
    
    def get(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'status': 'success',
                'detail': "Logged in successfully!",
                'user': {
                    'email': user.email,
                    'username': user.username
                    },
                'token': token.key
            }, status=status.HTTP_202_ACCEPTED)
        return Response({
            'status': 'error',
            'detail': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
            
            
            
        

        
    
 