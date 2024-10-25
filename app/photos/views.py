from django.contrib.auth import get_user_model, authenticate

from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

from core import models
from photos import serializers


@api_view(['GET'])
def photo_view(request):
    photos = models.Photos.objects.all()
    serializer = serializers.PhotoSerializer(photos, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

