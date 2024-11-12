from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    renderer_classes,
)
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
@renderer_classes(api_settings.DEFAULT_RENDERER_CLASSES)
def create_token(request):
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        user_serial = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user_serial)
        return Response({'Token': token.key}, status.HTTP_201_CREATED)

    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    user = request.user

    if not user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == 'PATCH':
        serializer = UserSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
