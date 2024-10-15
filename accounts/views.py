# views.py
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

CustomUser = get_user_model()

class RegisterView(generics.CreateAPIView):
    """View to handle user registration."""
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class CustomLoginView(APIView):
    """View to handle user login and JWT token generation."""
    @swagger_auto_schema(
        request_body=LoginSerializer,  # Specify the request body
        responses={200: 'Login successful', 400: 'Invalid credentials'}
    )
    def post(self, request, *args, **kwargs):
        # Use the LoginSerializer to validate the request data
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # If the data is valid, return the tokens and user info
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """View to handle user logout by blacklisting the JWT token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from the request data
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
