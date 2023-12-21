"""
Models for the E-commerce App
"""
import uuid
import os

from PIL import Image

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def profile_image_file_path(instance, filename):
    """Generate file path for new image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'profile_images', filename)


def product_image_file_path(instance, filename):
    """Generate file path for new image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'product', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""

        if not email:
            raise ValueError("User must have an email address.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create, save and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="First Name")
    last_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Last Name")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='date joined')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Profile(models.Model):
    """User Profile object."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)

    def __str__(self):
        """Return the name of the user."""
        return self.username

    @property
    def username(self):
        """Make a username property."""
        return self.user.email


class Product(models.Model):
    """Product object."""
    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    discount = models.IntegerField(blank=True, null=True, default=0)
    rating = models.IntegerField(null=True, blank=True, default=1)
    large_image = models.ImageField(null=True, default="uploads/products/1.jpg",
                                    upload_to=product_image_file_path)

    def __str__(self):
        return self.title

    # resizing images
    def save(self, *args, **kwargs):
        """Save a smaller image."""
        super().save()

        large_image = Image.open(self.large_image.path)

        if large_image.width != 300 and large_image.height != 300:
            new_img = (300, 300)
            large_image.thumbnail(new_img)
            large_image.save(self.large_image.path)


class Order(models.Model):
    items = models.CharField(max_length=1000)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    total = models.CharField(max_length=200)
