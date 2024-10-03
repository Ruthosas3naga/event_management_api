from django_filters import rest_framework as filters
from .models import Event

class EventFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')  # Case-insensitive search
    location = filters.CharFilter(field_name="location", lookup_expr='icontains')  # Case-insensitive search
    date_time = filters.DateFromToRangeFilter(field_name="date_time")  # Filter by date range

    class Meta:
        model = Event
        fields = ['title', 'location', 'date_time']