"""
Tests for the user API.
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

INDEX_URL = reverse('shop:index')
CHECKOUT_URL = reverse('shop:checkout')


# TODO
# REMOVE_FROM_CART
# ADD_TO_WISHLIST
# REMOVE_FROM_WISHLIST
# ORDERED


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicShopTests(TestCase):
    """Test the public features of the shop."""

    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        """Test for the index page successful."""
        res = self.client.get(INDEX_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateShopTests(TestCase):
    """Test for shop that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
        )
        self.client = Client()
        self.client.force_login(user=self.user)
