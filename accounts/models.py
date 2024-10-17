# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom manager to handle user creation.
    """
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,  # Corrected from 'user' to 'username'
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None):
        # Use create_user instead of calling create_superuser recursively
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user




# class CustomUser(AbstractUser):
#     """
#     Custom User model extending AbstractUser.
#     """
#     phone_number = models.CharField(max_length=255, blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     email = models.EmailField(max_length=255, unique=True)  # Make email unique

#     objects = CustomUserManager()  # Use the custom manager

#     def __str__(self):
#         return self.username

