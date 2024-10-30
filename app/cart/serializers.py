from core.models import Cart

from rest_framework import serializers


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'photo', 'price', 'quantity']

    def update(self, instance, validated_data):
        """Update quantity of cart."""
        new_quantity = validated_data.pop('quantity', None)
        cart = super().update(instance, validated_data)
        cart.quantity = new_quantity

        return cart