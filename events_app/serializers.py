from .models import Event, Comment, Notification
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, attrs):
        # To ensure title, date_time, and location are provided
        if not attrs.get('title'):
            raise serializers.ValidationError("Title is required.")
        if not attrs.get('date_time'):
            raise serializers.ValidationError("Date and Time are required.")
        if not attrs.get('location'):
            raise serializers.ValidationError("Location is required.")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'event', 'content', 'created_date']
        read_only_fields = ['user', 'created_date']

    # Assign user in the view or handle logic elsewhere if needed


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user', 'message', 'created_date', 'is_read'] 
        read_only_fields = ['is_read', 'created_date']
