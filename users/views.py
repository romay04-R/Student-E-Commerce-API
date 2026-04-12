from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Sum
from .models import UserProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, 
    PublicUserProfileSerializer, UserStatsSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_stats(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    from products.models import Product
    from orders.models import Order
    
    stats = {
        'total_products': Product.objects.filter(user=user).count(),
        'active_products': Product.objects.filter(user=user, is_active=True).count(),
        'total_orders': Order.objects.filter(buyer=user).count(),
        'completed_orders': Order.objects.filter(buyer=user, status='completed').count(),
        'total_sales': profile.total_sales,
        'average_rating': profile.average_rating,
        'total_reviews': 0  # Will be calculated below
    }
    
    # Calculate total reviews
    from products.models import ProductReview
    stats['total_reviews'] = ProductReview.objects.filter(product__user=user).count()
    
    serializer = UserStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_user_by_id(request, userId):
    try:
        profile = UserProfile.objects.get(id=userId)
        serializer = PublicUserProfileSerializer(profile)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_user_rating(request, userId):
    try:
        profile = UserProfile.objects.get(id=userId)
        
        from products.models import ProductReview
        reviews = ProductReview.objects.filter(product__user=profile.user)
        
        rating_data = {
            'average_rating': profile.average_rating,
            'total_reviews': reviews.count(),
            'rating_distribution': {}
        }
        
        # Calculate rating distribution
        for i in range(1, 6):
            rating_data['rating_distribution'][str(i)] = reviews.filter(rating=i).count()
        
        return Response(rating_data)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
