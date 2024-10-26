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


class Photos(models.Model):
    """Photo object."""
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=1024)
    photo_path = models.CharField(max_length=200, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Prices(models.Model):
    """Price for each photo size."""
    photo = models.ForeignKey(Photos, on_delete=models.CASCADE)
    size = models.CharField(max_length=15)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.size + ' of ' + self.photo.title + 'is $' + str(self.price)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photos, on_delete=models.CASCADE)
    price = models.ForeignKey(Prices, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
