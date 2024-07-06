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
                             'data': {'accessToken': str(token.access_token),
                                      'user': UserSerializer(user).data}},
                            status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad'
        })
