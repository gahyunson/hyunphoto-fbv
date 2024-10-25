from core.models import Cart

from rest_framework import serializers


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'photo', 'price', 'quantity']