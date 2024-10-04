from django.urls import path, include
from . views import EventDetailView, EventListCreateView, EventRegistrationView, CommentListCreateView

urlpatterns = [
    path('events/', EventListCreateView.as_view()),
    path('events/<int:pk>', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/register/', EventRegistrationView.as_view(), name='event-register'),
    path('events/<int:event-id>/comments/', CommentListCreateView.as_view(), name='event-comments'),
]