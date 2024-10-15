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


urlpatterns = [
    # Event-related URLs
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/register/', EventRegistrationView.as_view(), name='event-register'),
    path('events/<int:pk>/comments/', CommentListCreateView.as_view(), name='event-comments'),

    # Comment-related URLs 
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'), 

    # Notification-related URLs 
    path('notifications/', NotificationListView.as_view(), name='notification-list'),  
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'), 
    path('notifications/<int:pk>/mark-as-read/', NotificationMarkAsReadView.as_view(), name='notification-mark-as-read'),
]       
