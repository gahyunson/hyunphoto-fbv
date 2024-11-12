from rest_framework import serializers

from core.models import Photos, Prices


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = ['id', 'photo', 'size', 'price']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ['id', 'title', 'image']


class PhotoDetailSerializer(PhotoSerializer):
    photo_price = PriceSerializer(many=True)

    class Meta(PhotoSerializer.Meta):
        fields = PhotoSerializer.Meta.fields + ['description', 'photo_price']
