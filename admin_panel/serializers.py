from rest_framework import serializers
from django.contrib.auth.models import User
from products.models import Product
from .models import ReportedUser, ReportedProduct


class UserStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    suspended_users = serializers.IntegerField()
    total_products = serializers.IntegerField()
    pending_products = serializers.IntegerField()
    total_orders = serializers.IntegerField()
    pending_orders = serializers.IntegerField()


class ReportedUserSerializer(serializers.ModelSerializer):
    reported_username = serializers.CharField(source='reported_user.username', read_only=True)
    reporter_username = serializers.CharField(source='reporter.username', read_only=True)
    
    class Meta:
        model = ReportedUser
        fields = '__all__'


class ReportedProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    reporter_username = serializers.CharField(source='reporter.username', read_only=True)
    
    class Meta:
        model = ReportedProduct
        fields = '__all__'


class AdminUserSerializer(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    order_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'is_active', 'date_joined', 'profile_data', 'product_count', 'order_count')
    
    def get_profile_data(self, obj):
        try:
            profile = obj.userprofile
            return {
                'phone': profile.phone,
                'address': profile.address,
                'date_of_birth': profile.date_of_birth
            }
        except:
            return {}
    
    def get_product_count(self, obj):
        from products.models import Product
        return Product.objects.filter(is_active=True).count()
    
    def get_order_count(self, obj):
        from orders.models import Order
        return Order.objects.filter(user=obj).count()
