from rest_framework import status, authentication, permissions
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

from core.models import Cart
from cart.serializers import CartSerializer


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def cart_list(request):
    if not request.user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    elif request.method == 'PATCH':
        cart_id = request.data.get('cart_id')
        new_quantity = request.data.get('quantity')
        cart = Cart.objects.get(id=cart_id)

        serializer = CartSerializer(cart, data={'quantity': new_quantity}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
