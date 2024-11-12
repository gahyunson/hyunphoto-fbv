"""Tests for photos APIs."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient
import tempfile

from core.models import (
    Photos,
    Prices
)
from photos import serializers


PHOTOS_URL = reverse('photos:photos-list')


def detail_url(photo_id):
    return reverse('photos:photo-detail', args=[photo_id])


def create_photos(**params):
    """Create and return a photo sample data."""
    sample = {
        'title': 'The night',
        'description': 'The night we used to rock.',
        'image': tempfile.NamedTemporaryFile(suffix=".jpg").name
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


def create_superuser(**params):
    """Create and return a superuser."""
    return get_user_model().objects.create_superuser(**params)


class PublicPhotoPriceApiTests(TestCase):
    """Test authenticated API."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_superuser(email='admin@example.com',
                                     password='admin123')
        self.client.force_authenticate(self.user)

    def test_photos_list(self):
        """Test get a list of photos."""
        create_photos()
        sample = {'title': 'New York City'}
        create_photos(**sample)

        res = self.client.get(PHOTOS_URL)

        photos = Photos.objects.all()
        serializer = serializers.PhotoSerializer(photos, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), len(serializer.data))

    def test_price_of_photo_list(self):
        photo1 = create_photos()
        create_prices(photo1)

        url = detail_url(photo1.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_photo_detail(self):
        """Test getting photo detail."""
        photo = create_photos()
        create_prices(photo)

        price_sample = {
            'size': '40x32"',
            'price': 160.0
        }
        create_prices(photo, **price_sample)

        url = detail_url(photo.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data[0]['title'], photo)
        self.assertEqual(len(res.data[0]['photo_price']), 2)
