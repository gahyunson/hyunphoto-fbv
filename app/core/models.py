from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_field):
        """Create and return a new user."""
        if not email:
            raise ValueError('The email field must be set.')
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True, null=True)
    address2 = models.TextField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    nation = models.CharField(max_length=100, blank=True, null=True)
    postal = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'