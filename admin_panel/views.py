from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from products.models import Product
from orders.models import Order
from .models import ReportedUser, ReportedProduct
from .serializers import (
    UserStatsSerializer, ReportedUserSerializer, 
    ReportedProductSerializer, AdminUserSerializer
)


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_statistics(request):
    stats = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'suspended_users': User.objects.filter(is_active=False).count(),
        'total_products': Product.objects.count(),
        'pending_products': Product.objects.filter(is_active=False).count(),
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
    }
    
    serializer = UserStatsSerializer(stats)
    return Response(serializer.data)


class PendingProductsListView(generics.ListAPIView):
    serializer_class = ReportedProductSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return Product.objects.filter(is_active=False)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def approve_product(request, productId):
    try:
        product = Product.objects.get(id=productId)
        product.is_active = True
        product.save()
        return Response({'status': 'Product approved'})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def reject_product(request, productId):
    try:
        product = Product.objects.get(id=productId)
        product.delete()
        return Response({'status': 'Product rejected and deleted'})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class ReportedUsersListView(generics.ListAPIView):
    serializer_class = ReportedUserSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        status_filter = self.request.query_params.get('status', None)
        queryset = ReportedUser.objects.all()
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset.order_by('-created_at')


class ReportedProductsListView(generics.ListAPIView):
    serializer_class = ReportedProductSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        status_filter = self.request.query_params.get('status', None)
        queryset = ReportedProduct.objects.all()
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset.order_by('-created_at')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def suspend_user(request, userId):
    try:
        user = User.objects.get(id=userId)
        user.is_active = False
        user.save()
        
        # Update reported user status
        reported_user = ReportedUser.objects.filter(reported_user=user).first()
        if reported_user:
            reported_user.status = 'suspended'
            reported_user.save()
        
        return Response({'status': 'User suspended'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def remove_product(request, productId):
    try:
        product = Product.objects.get(id=productId)
        product.delete()
        return Response({'status': 'Product removed'})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def unsuspend_user(request, userId):
    try:
        user = User.objects.get(id=userId)
        user.is_active = True
        user.save()
        
        # Update reported user status
        reported_user = ReportedUser.objects.filter(reported_user=user).first()
        if reported_user:
            reported_user.status = 'cleared'
            reported_user.save()
        
        return Response({'status': 'User unsuspended'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class AdminUsersListView(generics.ListAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        status_filter = self.request.query_params.get('status', None)
        role_filter = self.request.query_params.get('role', None)
        
        queryset = User.objects.all()
        
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'suspended':
            queryset = queryset.filter(is_active=False)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        if role_filter == 'admin':
            queryset = queryset.filter(is_staff=True)
        elif role_filter == 'student':
            queryset = queryset.filter(is_staff=False)
        
        return queryset.order_by('-date_joined')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def report_product(request, productId):
    try:
        product = Product.objects.get(id=productId)
        reason = request.data.get('reason', '')
        
        if not reason:
            return Response({'error': 'Reason is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already reported
        existing_report = ReportedProduct.objects.filter(
            product=product, reporter=request.user
        ).first()
        
        if existing_report:
            return Response({'error': 'You have already reported this product'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        report = ReportedProduct.objects.create(
            product=product,
            reporter=request.user,
            reason=reason
        )
        
        return Response({'status': 'Product reported successfully'}, status=status.HTTP_201_CREATED)
        
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def report_user(request, userId):
    try:
        reported_user = User.objects.get(id=userId)
        reason = request.data.get('reason', '')
        
        if not reason:
            return Response({'error': 'Reason is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already reported
        existing_report = ReportedUser.objects.filter(
            reported_user=reported_user, reporter=request.user
        ).first()
        
        if existing_report:
            return Response({'error': 'You have already reported this user'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        report = ReportedUser.objects.create(
            reported_user=reported_user,
            reporter=request.user,
            reason=reason
        )
        
        return Response({'status': 'User reported successfully'}, status=status.HTTP_201_CREATED)
        
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
