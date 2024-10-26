from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


# def create_user(email='user@example.com', password='test123'):
#     """Create and return a new user."""
#     return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'test123test'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, normal_email in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, normal_email)

    def test_create_user_without_email_error(self):
        """Error test when create a user without an email, ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_superuser_successful(self):
        """Test creating a superuser is successful."""
        user = get_user_model().objects.create_superuser(
            'admin@example.com',
            'admin123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_photo_create_successful(self):
        """Test creating a photo is successful."""
        title = 'The night'
        description = 'The night we used to rock.'
        photo_path = 'static/thenight.png'
        photos = models.Photos.objects.create(
            title = title,
            description = description,
            photo_path = photo_path
        )
        self.assertEqual(str(photos), title)

    def test_price_create_successful(self):
        """Test creating a price is successful."""
        photo = models.Photos.objects.create(
            title = 'The night',
            description = 'The night we used to rock.',
            photo_path = 'static/thenight.png'
        )
        size = '20x16"'
        price = 88.0
        prices = models.Prices.objects.create(photo = photo,
                                              size = size,
                                              price = price)
        self.assertEqual(prices.price, 88.0)
