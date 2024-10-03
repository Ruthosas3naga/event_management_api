from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_future_date(value):
    if value < timezone.now():
        raise ValidationError('The time cannot be in the past')

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_time = models.DateTimeField(validators=[validate_future_date])
    organizer = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    registered_users = models.ManyToManyField(CustomUser, related_name='registered_events', blank=True)

    class Meta:
        verbose_name_plural = "Events"
        ordering = ['date_time']

    def __str__(self): 
        return self.title
    
    def is_past_event(self):
        """To check if the event date_time is in the past"""
        return self.date_time < timezone.now()

    def register_user(self, user):
        """Register a user for the event if capacity allows"""
        if self.capacity > 0:
            self.registered_users.add(user)
            self.capacity -= 1
            self.save()
        else:
            raise ValidationError("Event is at full capacity")
