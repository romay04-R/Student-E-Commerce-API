from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT serializer that includes user data in the token"""
    
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        
        # Add custom claims
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        
        # Add user profile data if exists
        if hasattr(user, 'userprofile'):
            profile = user.userprofile
            token['role'] = profile.role
            token['profile_id'] = str(profile.id)  # UUID as string
            token['is_seller'] = profile.is_seller
            token['average_rating'] = str(profile.average_rating)
            token['total_sales'] = str(profile.total_sales)
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user data to response
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        
        # Add user info to response
        user = self.user
        data['user'] = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        }
        
        # Add profile info if exists
        if hasattr(user, 'userprofile'):
            profile = user.userprofile
            data['user']['role'] = profile.role
            data['user']['profile'] = {
                'id': str(profile.id),
                'is_seller': profile.is_seller,
                'average_rating': float(profile.average_rating),
                'total_sales': float(profile.total_sales),
            }
        
        return data


class CustomTokenRefreshSerializer(serializers.Serializer):
    """Custom refresh token serializer"""
    refresh = serializers.CharField()
    
    def validate(self, attrs):
        refresh = attrs['refresh']
        
        token = RefreshToken(refresh)
        
        data = {
            'access': str(token.access_token),
            'refresh': refresh,
        }
        
        return data
