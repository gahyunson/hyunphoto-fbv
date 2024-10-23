from django.contrib.auth import get_user_model, authenticate

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_token(request):
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
        return Response({'Token': token.key}, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
