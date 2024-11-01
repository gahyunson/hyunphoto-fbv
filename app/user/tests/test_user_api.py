from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)


SIGNUP_USER_URL = reverse('user:signup')
TOKEN_URL = reverse('user:token')
PROFILE_URL = reverse('user:profile')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test Public User API."""
    def setUp(self):
        self.client = APIClient()

    def test_signup_user_success(self):
        """Test creating/signup a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass1234',
            'name': 'Test Name',
        }
        res = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_signup_user_exist_error(self):
        """Test signup a user is fail, email already exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass1234',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_user_password_short_error(self):
        """Test signup a user is fail, password is too short."""
        payload = {
            'email': 'test@example.com',
            'password': '123',
            'name': 'Test Name',
        }
        res = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user_success(self):
        """Test generates token for valid credentials."""
        user_details = {
            'email': 'test@example.com',
            'password': 'testpass1234',
            'name': 'Test Name',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('Token', res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_token_crendentials_invalid(self):
        """Test returns error if credentials invalid."""
        user_details = {
            'email': 'test@example.com',
            'password': 'testpass1234',
            'name': 'Test Name',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': 'yougotthewrongnumber',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('Token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_password_blank(self):
        """Test returns an error if password blank."""
        payload = {
            'email': 'test@example.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('Token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Test returns error if email not found."""
        payload = {
            'email': 'unittest@example.com',
            'password': 'testpass1234',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('Token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    """Test User API that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_info_success(self):
        """Test retrieving user info who logged in."""
        res = self.client.get(PROFILE_URL)

        check_user = {'name': self.user.name, 'email': self.user.email}

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, check_user)

    def test_update_user_info_success(self):
        """Test update user info success."""
        payload = {
            'name': 'New Jeans', 'password': 'newpassword'
        }
        res = self.client.patch(PROFILE_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_user_success(self):
        """Test delete user success."""
        res = self.client.delete(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        User = get_user_model()
        user_exists = User.objects.filter(email=self.user.email)
        self.assertFalse(user_exists.exists())

    def test_delete_user_fail_when_logout(self):
        self.client.logout()
        res = self.client.delete(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
