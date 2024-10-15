from django.shortcuts import render
from rest_framework.response import Response
from .serializers import EventSerializer, CommentSerializer, NotificationSerializer, EventRegistrationSerializer
from . models import Event, Comment, Notification
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.pagination import PageNumberPagination
from .filters import EventFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend


class EventPagination(PageNumberPagination):
    """Custom pagination for event list."""
    page_size = 5

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to allow only the owner of an object to edit it."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer == request.user.username
    
    #CRUD OPERATIONS

class EventListCreateView(generics.ListCreateAPIView):
    """Handles listing and creating events."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_class = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = EventPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = EventFilter
    # List all events (GET)
    def get(self, request, *args, **kwargs):
        events = self.get_queryset()
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a new event (POST)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """Sets the event organizer to the current user."""
    def perform_create(self, serializer):  
        serializer.save(organizer=self.request.user.username)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting an event."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]
    

    # Retrieve a specific event (GET)
    def get(self, request, *args, **kwargs):
        try:
            event = self.get_object()
            serializer = self.get_serializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            raise NotFound(detail="Event not found")

# Update a specific event (PUT)
    def put(self, request, *args, **kwargs):
        try:
            event = self.get_object()
            if event.organizer != request.user.username:
                raise PermissionDenied("You do not have permission to edit this event.")
            serializer = self.get_serializer(event, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            raise NotFound(detail="Event not found")


    def perform_update(self, serializer):
        """Ensure that the user updating the event is the organizer."""
        if self.get_object().organizer !=self.request:
            raise PermissionDenied("You do ot ahave access to this service")
        serializer.save()

    def perform_destroy(self, instance):
       """Ensure that the user deleting the event is the organizer."""
       if instance.organizer != self.request.user.username:
           raise PermissionDenied("You do not have access to this service")
       instance.delete()

  
class EventRegistrationView(generics.UpdateAPIView):
    """Handles event registration."""
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return EventRegistrationSerializer
    # permission_classes = [IsAuthenticated]

    # def update(self, request, *args, **kwargs):
    #     event = self.get_object()
    #     user = event.user
    #     try:
    #         event.register_user
    #         return Response({"message": "Registration successful"})
    #     except ValidationError as e:
    #         return Response({"error": str(e)}, status=400)


class CommentListCreateView(generics.ListCreateAPIView):
    """Handles listing and creating comments for events."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes =[IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting a comment."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Optional: Limit comments to the authenticated user
        user = self.request.user
        return self.queryset.filter(user=user)  # Optional: only allow users to modify their comments

class NotificationListView(generics.ListAPIView):
    """Handles listing notifications for the authenticated user."""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    

    def get_queryset(self):
        """Return notifications for the current authenticated user."""
        return Notification.objects.filter(user=self.request.user).order_by('-created_date')

class NotificationDetailView(generics.RetrieveAPIView):
    """Handles retrieving a specific notification."""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]


class NotificationMarkAsReadView(generics.UpdateAPIView):
    """Marks a notification as read."""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """Mark the notification as read."""
        instance = serializer.save(is_read=True)