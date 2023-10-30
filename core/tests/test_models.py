"""
Test Models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """ Test models."""

    def test_create_user_with_email_successful(self):
        """ Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Tests that creating a new user without an email
        raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """ Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            "admin@example.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    #
    # def test_create_product_successful(self):
    #     """ Test creating a product is successful."""
    #
    #     user = get_user_model().objects.create_user(
    #         'test@example.com',
    #         'testpass123',
    #     )
    #
    #     product = models.Product.objects.create(
    #         user=user,
    #         title='Sample product title',
    #         price=float('50.99'),
    #         discount=float('18.50'),
    #         description='Sample product description.',
    #         category='Shoes',
    #     )
    #
    #     self.assertEqual(str(product), product.title)
