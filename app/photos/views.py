from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.models import Photos, Prices
from photos import serializers


@api_view(['GET'])
def photo_list(request):
    try:
        photos = Photos.objects.all()
        serializer = serializers.PhotoSerializer(photos, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    except Photos.DoesNotExist:
        return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def photo_detail(request, photo_id):
    try:
        photo = Photos.objects.get(id=photo_id)
        serializer = serializers.PhotoDetailSerializer(photo)
        return Response(serializer.data, status.HTTP_200_OK)
    except Photos.DoesNotExist:
        return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

