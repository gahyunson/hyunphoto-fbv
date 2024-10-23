from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


SIGNUP_USER_URL = reverse('user:signup')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
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

    def test_create_token_for_user(self):
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

