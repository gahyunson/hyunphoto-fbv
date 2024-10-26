"""Tests for cart APIs."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Photos, Prices, Cart

from cart.serializers import CartSerializer

CART_URL = reverse('cart:cart-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_photos(**params):
    """Create and return a photo sample data."""
    sample = {
        'title': 'The night',
        'description': 'The night we used to rock.',
        'photo_path': 'static/thenight.png'
    }
    sample.update(params)
    photo = Photos.objects.create(**sample)

    return photo


def create_prices(photo, **params):
    price_sample = {
        'photo': photo,
        'size': '20x16"',
        'price': 86.0
    }
    price_sample.update(params)
    price = Prices.objects.create(**price_sample)

    return price


def create_cart(user, **params):
    """Create cart to my cart."""
    photo = create_photos()
    price = create_prices(photo)
    defaults = {
        'user': user,
        'photo': photo,
        'price': price,
        'quantity': 1
    }
    defaults.update(params)
    cart = Cart.objects.create(**defaults)

    return cart


class PrivateCartApiTests(TestCase):
    """Test cart API authenticated."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='gahyun@example.com', password='macbook')
        self.client.force_authenticate(self.user)

    def test_cart_list_success(self):
        create_cart(self.user)
        user2 = create_user(
            **{
                'email': 'user2@example.com',
                'password': 'user2123',
                'name': 'User Two'
            }
        )
        create_cart(user2)

        res = self.client.get(CART_URL)

        cart = Cart.objects.filter(user=self.user)
        serializer = CartSerializer(cart, many=True)
        # print(res.data, serializer.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), len(serializer.data))

    def test_cart_list_fail_unauthenticate(self):
        create_cart(self.user)

        user2 = self.client.force_authenticate(user=None)
        res = self.client.get(CART_URL)

        cart = Cart.objects.filter(user=user2)
        serializer = CartSerializer(cart, many=True)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(serializer.data)
