from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_future_date(value):
    if value < timezone.now():
        raise ValidationError('The time cannot be in the past')

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Notification for {self.user}: {self.message}'

    def mark_as_read(self):
        """Mark the notification as read."""
        self.is_read = True
        self.save()

# Updating the Event model to send notifications
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_time = models.DateTimeField(validators=[validate_future_date])
    organizer = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    registered_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='registered_events', blank=True)

    class Meta:
        verbose_name_plural = "Events"
        ordering = ['date_time']

    def __str__(self):
        return self.title

    def is_past_event(self):
        """Check if the event date_time is in the past."""
        return self.date_time < timezone.now()

    def register_user(self, user):
        """Register a user for the event if capacity allows and send a notification."""
        if self.capacity > self.registered_users.count():
            self.registered_users.add(user)
            self.save()
            # Create a notification for the user
            Notification.objects.create(
                user=user,
                message=f'You have successfully registered for {self.title} on {self.date_time}.'
            )
        else:
            raise ValidationError("Event is at full capacity")

    def unregister_user(self, user):
        """Unregister a user from the event and send a notification."""
        if user in self.registered_users.all():
            self.registered_users.remove(user)
            self.save()
            # Create a notification for the user
            Notification.objects.create(
                user=user,
                message=f'You have been unregistered from {self.title}.'
            )
        else:
            raise ValidationError("User is not registered for this event")



class Comment(models.Model):
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.event}'



