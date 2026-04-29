from rest_framework import serializers
from .models import Order, OrderItem, Payment
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = OrderItem
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['order', 'amount', 'paystack_reference', 'status', 'paid_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    product = serializers.SerializerMethodField()
    payment = PaymentSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['buyer', 'seller', 'total_amount', 'status']
    
    def get_product(self, obj):
        product = obj.get_product()
        if product:
            return ProductSerializer(product).data
        return None


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['items', 'notes']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        buyer = self.context['request'].user
        
        # Calculate total amount and get seller
        total_amount = 0
        seller = None
        
        for item_data in items_data:
            product = item_data['product']
            if isinstance(product, int):
                from products.models import Product
                product = Product.objects.get(id=product)
            
            total_amount += product.price * item_data['quantity']
            
            if seller is None:
                seller = product.user
            elif seller != product.user:
                raise serializers.ValidationError("All items must be from the same seller")
        
        order = Order.objects.create(
            buyer=buyer,
            seller=seller,
            total_amount=total_amount,
            notes=validated_data.get('notes', '')
        )
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order


class PaymentInitializeSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    email = serializers.EmailField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    callback_url = serializers.URLField(required=False)


class PaymentVerifySerializer(serializers.Serializer):
    reference = serializers.CharField()
