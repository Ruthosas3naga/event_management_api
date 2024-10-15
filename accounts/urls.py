from django.urls import path
from .views import RegisterView, CustomLoginView, LogoutView 

# URL patterns for user authentication
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]