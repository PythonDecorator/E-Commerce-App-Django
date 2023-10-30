"""
Tests for the user API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from ecom_apps.user.forms import SignUpForm, LoginForm

REGISTER_USER_URL = reverse('user:register')
LOGIN_USER_URL = reverse('user:login')
INDEX_PAGE_URL = reverse("shop:index")
LOGOUT_USER_URL = reverse('user:logout')
USER_PROFILE_URL = None
USER_EDIT_PROFILE_URL = None


# TODO
# USER_DELETE_ACCOUNT_URL = reverse('user:delete-account')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def detail_url(user_email):
    """Create and return a detail URL."""
    return reverse('user:profile', args=[user_email])


def update_url(user_email):
    """Create and return a detail URL."""
    return reverse('user:profile-update', args=[user_email])


class PublicUserViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_view_success(self):
        """Test that registering a user with valid
        credentials is successful."""
        payload = {
            'email': 'test@example.com',
            'password1': "test123@pass",
            'password2': "test123@pass",
            'first_name': "Test",
            'last_name': "Test",
        }

        form = SignUpForm(payload)
        self.assertTrue(form.is_valid())

        res = self.client.post(REGISTER_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(res, LOGIN_USER_URL)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(payload['password1']))

    def test_user_with_email_exist_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password1': "test123@pass",
            'password2': "test123@pass",
        }

        form = SignUpForm(payload)
        self.assertTrue(form.is_valid())

        res = self.client.post(REGISTER_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)

        with self.assertRaises(Exception):
            user = create_user(email=payload['email'], password=payload['password1'])
            self.assertIsNotNone(user)
            self.assertTrue(user.check_password(payload['password1']))

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': "ph34@",
        }
        form = SignUpForm(payload)
        self.assertFalse(form.is_valid())

    def test_login_success(self):
        """Test user login is successful and
        redirected to the home page."""
        payload = {
            'email': 'test@example.com',
            'password': "test123@pass",
        }

        create_user(**payload)

        form = LoginForm(payload)
        self.assertTrue(form.is_valid())

        res = self.client.post(LOGIN_USER_URL, payload)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertTrue(user.is_authenticated)
        self.assertRedirects(res, INDEX_PAGE_URL)

    def test_login_with_bad_credentials_error(self):
        """Test returns error if credentials invalid."""
        create_user(email='test@example.com', password='good_pass')

        payload = {'email': 'test@example.com', 'password': 'bad_pass'}

        form = LoginForm(payload)
        self.assertTrue(form.is_valid())

        res = self.client.post(LOGIN_USER_URL, payload)
        self.assertNotEqual(res.status_code, status.HTTP_302_FOUND)

    def test_view_profile_unauthenticated_error(self):
        """Test authentication is required for users."""
        res = self.client.get(detail_url(user_email="test@example.com"))
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)


class PrivateUserViewTestCase(TestCase):
    """Test that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
        )
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_view_profile_success(self):
        """Test viewing profile for logged-in user."""
        url = detail_url(user_email=self.user.email)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, self.user.email)

    def test_logout_success(self):
        """Test for logging out user."""
        res = self.client.get(LOGOUT_USER_URL)
        self.assertTrue(self.user.is_authenticated)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
