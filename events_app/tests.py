from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Notification, Event, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationModelTests(TestCase):
    def setUp(self):
        """Create a test user and notification."""
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )
        self.notification = Notification.objects.create(
            user=self.user,
            message='This is a test notification.'
        )

    def test_notification_str(self):
        """Test the string representation of the notification."""
        self.assertEqual(str(self.notification), f'Notification for {self.user}: This is a test notification.')

class EventModelTests(TestCase):
    def setUp(self):
        """Create a test user and an event."""
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='A test event description.',
            date_time=timezone.now() + timezone.timedelta(days=1),  # Future date
            organizer='Organizer Name',
            capacity=2,
            location='Test Location'
        )

    def test_event_str(self):
        """Test the string representation of the event."""
        self.assertEqual(str(self.event), 'Test Event')

    def test_event_capacity(self):
        """Test user registration within capacity."""
        self.event.register_user(self.user)
        self.assertIn(self.user, self.event.registered_users.all())
        self.assertEqual(self.event.registered_users.count(), 1)

    def test_event_capacity_exceeded(self):
        """Test that registration fails when capacity is exceeded."""
        self.event.register_user(self.user)
        another_user = User.objects.create_user(
            username='anotheruser',
            password='password123',
            email='anotheruser@example.com'
        )
        self.event.register_user(another_user)
        with self.assertRaises(ValidationError):
            self.event.register_user(self.user)  # Should raise error

    def test_event_unregister_user(self):
        """Test that a user can unregister from an event."""
        self.event.register_user(self.user)
        self.event.unregister_user(self.user)
        self.assertNotIn(self.user, self.event.registered_users.all())

    def test_event_unregister_user_not_registered(self):
        """Test that unregistering a user not registered raises an error."""
        with self.assertRaises(ValidationError):
            self.event.unregister_user(self.user)  # Should raise error

    def test_event_is_past_event(self):
        """Test is_past_event method."""
        past_event = Event.objects.create(
            title='Past Event',
            date_time=timezone.now() - timezone.timedelta(days=1),
            organizer='Past Organizer',
            capacity=1,
            location='Past Location'
        )
        self.assertTrue(past_event.is_past_event())
        self.assertFalse(self.event.is_past_event())

class CommentModelTests(TestCase):
    def setUp(self):
        """Create a test user, event, and comment."""
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='A test event description.',
            date_time=timezone.now() + timezone.timedelta(days=1),
            organizer='Organizer Name',
            capacity=2,
            location='Test Location'
        )
        self.comment = Comment.objects.create(
            event=self.event,
            user=self.user,
            content='This is a test comment.'
        )

    def test_comment_str(self):
        """Test the string representation of the comment."""
        self.assertEqual(str(self.comment), f'Comment by {self.user} on {self.event}')

