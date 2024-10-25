from core.models import Photos, Prices

from rest_framework import serializers


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ['title', 'description', 'photo_path']


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
