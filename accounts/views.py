from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            return Response({'status': 'success',
                             'message': 'User successfully registered',
                             'data': {'accessToken': str(token.get_token_backend),
                                      'user': UserSerializer(user).data}},
                            status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'Registration Unsuccessful',
            'statusCode': 400,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            token = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Login Successful',
                'data': {
                    'accessToken': str(token.get_token_backend),
                    'user': self.serializer_class(user).data,
                }
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Bad request',
            'message': 'Authentication failed',
            'statusCode': 401
        }, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = User.objects.filter(pk=pk, id=request.user.id).first()

        if user and user.id == request.user.id:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            'status': 'Not found',
            'message': 'User not found',
            'statusCode': 404
        }, status=status.HTTP_404_NOT_FOUND)

