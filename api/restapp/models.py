
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
    name = models.CharField(unique=True, max_length=75)
    description = models.TextField()
    cover_image_key = models.CharField(unique=True, max_length=256)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return self.name


class AlbumPage(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=False, null=False)
    page_image_key = models.CharField(unique=True, max_length=256, null=False)


class Artifact(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=False)
    caption = models.TextField()
    details = models.TextField()
    date = models.DateField()
    primary_image_key = models.CharField(unique=True, max_length=256)
    secondary_image_key = models.CharField(unique=True, max_length=256)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False)
    Artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, blank=False)
    message = models.TextField()


class Personage(models.Model):
    name = models.TextField()
    artifacts = models.ManyToManyField(Artifact)
