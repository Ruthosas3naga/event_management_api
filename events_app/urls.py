from django.urls import path
from .views import (
    EventDetailView,
    EventListCreateView,
    EventRegistrationView,
    CommentListCreateView,
    NotificationDetailView,
    NotificationListView,
    NotificationMarkAsReadView,
    CommentDetailView
)
from rest_framework.authtoken.views import obtain_auth_token

# other imports and view definitions


urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/register/', EventRegistrationView.as_view(), name='event-register'),
    path('events/<int:pk>/comments/', CommentListCreateView.as_view(), name='event-comments'),  # Added comma here
    path('notifications/', NotificationListView.as_view(), name='notification-list'),  # List all notifications
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),  # Retrieve, update, and delete
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),  # Retrieve a single notification
    path('notifications/<int:pk>/mark-as-read/', NotificationMarkAsReadView.as_view(), name='notification-mark-as-read'),  # Mark a notification as read
]
