from .models import Event
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    #This is to check if title, date_time and location (attributes) are inputed
    def validate(self, attrs):
        if not attrs.get('title'):
            raise serializers.ValidationError("Title is required.")
        if not attrs.get('date_time'):
            raise serializers.ValidationError("Date and Time are required.")
        if not attrs.get('location'):
            raise serializers.ValidationError("Location is required.")
        return attrs
    