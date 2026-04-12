from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, search_products, 
    get_products_by_category, get_user_products, ProductReviewViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'', ProductViewSet)
router.register(r'reviews', ProductReviewViewSet, basename='productreview')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', search_products, name='search-products'),
    path('category/<str:category>/', get_products_by_category, name='products-by-category'),
    path('user/<int:userId>/products/', get_user_products, name='user-products'),
]
