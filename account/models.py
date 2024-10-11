from django.db import models
from django.contrib.auth.models import AbstractUser

#class to create a user
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
