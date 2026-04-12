from rest_framework_simplejwt.views import TokenObtainPairView
from .jwt_serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT login view that includes user data in response"""
    serializer_class = CustomTokenObtainPairSerializer
