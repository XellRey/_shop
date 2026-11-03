from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField("телефон", max_length=20, null=True)

    def __str__(self):
        return self.username

