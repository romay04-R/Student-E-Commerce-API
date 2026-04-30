from rest_framework import serializers
from .models import Category, Product, ProductReview, ProductImage


class CategoryBulkCreateSerializer(serializers.Serializer):
    categories = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        ),
        min_length=1,
        max_length=50
    )
    
    def validate_categories(self, value):
        # Validate each category structure
        for category_data in value:
            if 'name' not in category_data:
                raise serializers.ValidationError("Each category must have a 'name' field")
            if not category_data['name'].strip():
                raise serializers.ValidationError("Category name cannot be empty")
            
            # Check for duplicate names in the request
            names = [cat['name'].lower() for cat in value]
            if len(names) != len(set(names)):
                raise serializers.ValidationError("Duplicate category names found in request")
        
        return value
    
    def create(self, validated_data):
        categories_data = validated_data['categories']
        created_categories = []
        
        for category_data in categories_data:
            # Extract name and description
            name = category_data['name'].strip()
            description = category_data.get('description', '').strip()
            
            # Check if category already exists
            try:
                category = Category.objects.get(name__iexact=name)
                # Category exists, add to response
                created_categories.append(category)
            except Category.DoesNotExist:
                # Category doesn't exist, create it
                category = Category.objects.create(
                    name=name,
                    description=description
                )
                created_categories.append(category)
        
        return created_categories


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_username = serializers.CharField(source='user.username', read_only=True)
    seller_info = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['user', 'views_count']
    
    def get_seller_info(self, obj):
        from users.serializers import PublicUserProfileSerializer
        from users.models import UserProfile
        profile, created = UserProfile.objects.get_or_create(user=obj.user)
        return PublicUserProfileSerializer(profile).data
    
    def get_average_rating(self, obj):
        return obj.average_rating()


class ProductCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Product
        exclude = ['user', 'views_count']
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        
        # Create ProductImage objects
        for image_data in images_data:
            product_image = ProductImage.objects.create(image=image_data)
            product.images.add(product_image)
        
        return product


class ProductReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = '__all__'
        read_only_fields = ['user', 'product']


class ProductReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
