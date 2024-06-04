from rest_framework.response import Response
from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import CreateUserSerializer, LoginUserSerializer, UserSerializer
from .models import User


# function for manage error details
def error_detail(e):
    errors = e.detail
    
    error_messages = []
    for field, messages in errors.items():
        error_messages.append(f'{field}: {messages[0].__str__()}')
    
    return error_messages

def get_user_jwt(user: User):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


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
                jwt_tokens = get_user_jwt(user)
                return Response({
                        'status': 'success',
                        'detail': "User registered successfully!",
                        'tokens': jwt_tokens
                        # "token": token.key
                    })

        except serializers.ValidationError as e:
            data = {
                'status': 'error',
                'detail': error_detail(e)
                }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        

# login view 
class LoginUserView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginUserSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            jwt_tokens = get_user_jwt(user)
            return Response({
                'status': 'success',
                'detail': "Logged in successfully!",
                'tokens': jwt_tokens
            }, status=status.HTTP_202_ACCEPTED)
        return Response({
            'status': 'error',
            'detail': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
            
            
class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        try:
            user = self.retrieve(request, *args, **kwargs).data
            if user.get('username') == request.user.username:
                return Response({
                            'status': 'success',
                            'data_type': "private",
                            "user": user,
                        })
            else:
                return Response({
                    'status': 'success',
                    'deta_type': "public",
                    "user": user.get('username'),
                })

        except serializers.ValidationError as e:
            data = {
                'status': 'error',
                'detail': error_detail(e)
                }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, *args, **kwargs):
        pass
        

    
 