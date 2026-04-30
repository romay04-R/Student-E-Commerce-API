from rest_framework import viewsets, filters, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Product, ProductReview, ProductImage
from .serializers import (
    CategorySerializer, CategoryBulkCreateSerializer, ProductSerializer, ProductCreateSerializer, 
    ProductReviewSerializer, ProductReviewUpdateSerializer, ProductImageSerializer
)
from users.permissions import IsSeller, IsBuyer, IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'bulk_create':
            return CategoryBulkCreateSerializer
        return CategorySerializer
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            categories = serializer.save()
            return Response(
                CategorySerializer(categories, many=True).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price', 'condition', 'location']
    search_fields = ['name', 'description', 'user__username']
    ordering_fields = ['price', 'created_at', 'name', 'views_count']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSeller()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        
        # Handle search parameter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search) | 
                Q(user__username__icontains=search)
            )
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        return ProductSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsBuyer])  # Only buyers can add reviews
    def add_review(self, request, pk=None):
        product = self.get_object()
        
        # Check if user already reviewed
        existing_review = ProductReview.objects.filter(product=product, user=request.user).first()
        if existing_review:
            return Response({'error': 'You have already reviewed this product'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        product = self.get_object()
        sort_by = request.query_params.get('sortBy', 'newest')
        
        reviews = product.reviews.all()
        
        if sort_by == 'rating-high':
            reviews = reviews.order_by('-rating')
        elif sort_by == 'rating-low':
            reviews = reviews.order_by('rating')
        else:  # newest
            reviews = reviews.order_by('-created_at')
        
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def images(self, request, pk=None):
        product = self.get_object()
        
        if product.user != request.user:
            return Response({'error': 'You can only upload images to your own products'}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        images = request.FILES.getlist('images')
        if not images:
            return Response({'error': 'No images provided'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_images = []
        for image in images:
            product_image = ProductImage.objects.create(image=image)
            product.images.add(product_image)
            uploaded_images.append(ProductImageSerializer(product_image).data)
        
        return Response(uploaded_images, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_products(request):
    query = request.query_params.get('q', '')
    category = request.query_params.get('category', None)
    page = int(request.query_params.get('page', 1))
    limit = int(request.query_params.get('limit', 20))
    sort_by = request.query_params.get('sortBy', 'newest')
    
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(user__username__icontains=query)
        )
    
    if category:
        products = products.filter(category__name=category)
    
    # Sorting
    if sort_by == 'price-low':
        products = products.order_by('price')
    elif sort_by == 'price-high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        # This would require more complex logic for average rating
        products = products.order_by('-created_at')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_products = products[start:end]
    
    serializer = ProductSerializer(paginated_products, many=True)
    return Response({
        'products': serializer.data,
        'total': products.count(),
        'page': page,
        'limit': limit
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products_by_category(request, category):
    page = int(request.query_params.get('page', 1))
    limit = int(request.query_params.get('limit', 20))
    sort_by = request.query_params.get('sortBy', 'newest')
    
    products = Product.objects.filter(is_active=True, category__name=category)
    
    # Sorting
    if sort_by == 'price-low':
        products = products.order_by('price')
    elif sort_by == 'price-high':
        products = products.order_by('-price')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_products = products[start:end]
    
    serializer = ProductSerializer(paginated_products, many=True)
    return Response({
        'products': serializer.data,
        'total': products.count(),
        'page': page,
        'limit': limit
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_products(request, userId):
    page = int(request.query_params.get('page', 1))
    limit = int(request.query_params.get('limit', 20))
    
    products = Product.objects.filter(is_active=True, user_id=userId)
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_products = products[start:end]
    
    serializer = ProductSerializer(paginated_products, many=True)
    return Response({
        'products': serializer.data,
        'total': products.count(),
        'page': page,
        'limit': limit
    })


class ProductReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ProductReview.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProductReviewUpdateSerializer
        return ProductReviewSerializer
    
    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        serializer.save(user=self.request.user, product_id=product_id)
