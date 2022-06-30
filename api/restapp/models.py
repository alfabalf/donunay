
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, max_length=75)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Album(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=75)
    description = models.TextField()
    cover_image_key = models.CharField(unique=True, max_length=256)

    def __str__(self):
        return self.name
