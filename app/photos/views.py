from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.models import Photos, Prices
from photos import serializers


@api_view(['GET'])
def photo_list(request):
    photos = Photos.objects.all()
    serializer = serializers.PhotoSerializer(photos, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def photo_detail(request, photo_id):
    prices = Prices.objects.filter(photo=photo_id)
    serializer = serializers.PriceSerializer(prices, many=True)
    return Response(serializer.data, status.HTTP_200_OK)
