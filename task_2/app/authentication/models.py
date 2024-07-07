from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.


class Organization(models.Model):
    orgId = models.CharField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200)


class CustomUser(AbstractUser):
    username = None
    userId = models.CharField(
        default=uuid.uuid4, unique=True, primary_key=True)
    email = models.EmailField(_("email address"), unique=True, )
    firstName = models.CharField(max_length=250, null=False)
    lastName = models.CharField(max_length=250, null=False)
    phone = models.CharField(max_length=11)
    organization = models.ManyToManyField(
        to=Organization, related_name='users')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstName", "lastName"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
