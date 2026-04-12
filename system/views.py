from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from django.db import connection
from products.models import Category


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Check if API is running and database is accessible"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return Response({
            'status': 'healthy',
            'message': 'API is running successfully',
            'database': 'connected'
        })
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'message': str(e),
            'database': 'disconnected'
        }, status=503)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    """Get all available product categories"""
    try:
        categories = Category.objects.all()
        category_data = []
        
        for category in categories:
            # Get product count for each category
            product_count = category.products.filter(is_active=True).count()
            
            category_data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'product_count': product_count
            })
        
        return Response({
            'categories': category_data,
            'total': len(category_data)
        })
    except Exception as e:
        return Response({
            'error': 'Failed to fetch categories',
            'message': str(e)
        }, status=500)
