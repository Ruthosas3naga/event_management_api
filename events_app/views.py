from django.shortcuts import render
from rest_framework.response import Response
from .serializers import EventSerializer, CommentSerializer, NotificationSerializer
from . models import Event, Comment, Notification
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.pagination import PageNumberPagination
from .filters import EventFilter
from django_filters.rest_framework import DjangoFilterBackend

#for pagination
class EventPagination(PageNumberPagination):
    page_size = 5

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer == request.user.username
    
    #CRUD OPERATIONS
#Create view
class EventListCreateView(generics.ListCreateAPIView):
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

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user.username)

#Get detail view
class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
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
        if self.get_object().organizer !=self.request:
            raise PermissionDenied("You do ot ahave access to this service")
        serializer.save()

    def perform_destroy(self, instance):
       if instance.organizer != self.request.user.username:
           raise PermissionDenied("You do not have access to this service")
       instance.delete()

#Update view  
class EventRegistrationView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        user = event.user
        try:
            event.register_user
            return Response({"message": "Registration successful"})
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes =[IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Optional: Limit comments to the authenticated user
        user = self.request.user
        return self.queryset.filter(user=user)  # Optional: only allow users to modify their comments

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    

    def get_queryset(self):
        """Return notifications for the current authenticated user."""
        return Notification.objects.filter(user=self.request.user).order_by('-created_date')

class NotificationDetailView(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

#UPDATE (Mark as READ)
class NotificationMarkAsReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """Mark the notification as read."""
        instance = serializer.save(is_read=True)