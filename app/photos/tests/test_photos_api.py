"""Tests for photos APIs."""
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Photos,
    Prices
)


PHOTOS_URL = reverse('photos:photos-list')

def create_photos(user, **params):
    """Create and return a photo sample data."""
    if not user.is_staff:
        return None
    sample = Photos.objects.create(
        title = 'The night',
        description = 'The night we used to rock.',
        photo_path = 'static/thenight.png'
    )

    photo = Photos.objects.create(**sample)
    return photo

def create_superuser(**params):
    """Create and return a superuser."""
    return get_user_model().objects.create_superuser(**params)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated API."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_superuser(email='admin@example.com',
                                     password='admin123')
        self.client.force_authenticate(self.user)

    def test_photos_list(self):
        """Test get a list of photos."""
        create_photos(user=self.user)

        res = self.client.get(PHOTOS_URL)

        photos = Photos.objects.all()
        serializer = PhotoSerializer(photos, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)