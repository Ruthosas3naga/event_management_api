from .models import Event, Comment, Notification
from rest_framework import serializers



class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model with validation for required fields."""
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date_time', 'organizer', 'capacity', 'location', 'created_date']

    def validate(self, attrs):
        """Validate that title, date_time, and location are provided."""
        if not attrs.get('title'):
            raise serializers.ValidationError("Title is required.")
        if not attrs.get('date_time'):
            raise serializers.ValidationError("Date and Time are required.")
        if not attrs.get('location'):
            raise serializers.ValidationError("Location is required.")
        return attrs

class EventRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for Event Registration model."""
    class Meta:
        Model = Event
        fields = ['id']

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    class Meta:
        model = Comment
        fields = ['id', 'event', 'content', 'created_date']
        read_only_fields = ['user', 'created_date']

  


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""
    class Meta:
        model = Notification
        fields = ['user', 'message', 'created_date', 'is_read'] 
        read_only_fields = ['is_read', 'created_date']

