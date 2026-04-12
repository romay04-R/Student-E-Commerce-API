from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'access', 'refresh')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True, 'min_length': 3}
        }
    
    def validate_username(self, value):
        # Username validation: alphanumeric + underscores, min 3 chars
        if not value.replace('_', '').isalnum():
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        if User.objects.filter(username__iexact=value).exists():
            raise ValidationError("A user with that username already exists.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError("A user with that email already exists.")
        return value
    
    def validate_password(self, value):
        # Password validation: at least 8 chars, one uppercase, one lowercase, one digit
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(c.isupper() for c in value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(c.islower() for c in value):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not any(c.isdigit() for c in value):
            raise ValidationError("Password must contain at least one digit.")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 as it's not a User model field
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # Add custom claims to tokens
        refresh['user_id'] = user.id
        refresh['username'] = user.username
        refresh['email'] = user.email
        refresh['first_name'] = user.first_name
        refresh['last_name'] = user.last_name
        refresh['is_staff'] = user.is_staff
        refresh['is_superuser'] = user.is_superuser
        
        # Add profile data if exists
        if hasattr(user, 'userprofile'):
            profile = user.userprofile
            refresh['profile_id'] = str(profile.id)
            refresh['is_seller'] = profile.is_seller
            refresh['average_rating'] = str(profile.average_rating)
            refresh['total_sales'] = str(profile.total_sales)
        
        # Add tokens to user object for serializer response
        user.access = str(refresh.access_token)
        user.refresh = str(refresh)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'address', 
                 'date_of_birth', 'bio', 'profile_picture', 'is_seller', 'average_rating', 
                 'total_sales', 'created_at')
    
    def update(self, instance, validated_data):
        # Extract user-related data
        user_data = {}
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
        
        # Update user fields
        user = instance.user
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        user.save()
        
        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class PublicUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'first_name', 'last_name', 'bio', 'profile_picture', 
                 'is_seller', 'average_rating', 'total_sales', 'created_at')


class UserStatsSerializer(serializers.Serializer):
    total_products = serializers.IntegerField()
    active_products = serializers.IntegerField()
    total_orders = serializers.IntegerField()
    completed_orders = serializers.IntegerField()
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    total_reviews = serializers.IntegerField()
