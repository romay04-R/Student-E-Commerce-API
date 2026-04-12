from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Q
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, OrderItemSerializer
from products.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['put'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        reason = request.data.get('reason', '')
        
        if order.status == 'pending':
            order.cancel_order(reason)
            return Response({'status': 'Order cancelled'})
        return Response({'error': 'Cannot cancel this order'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    items_data = request.data.get('items', [])
    notes = request.data.get('notes', '')
    
    if not items_data:
        return Response({'error': 'No items provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            # Calculate total amount and get seller
            total_amount = 0
            seller = None
            products_to_update = []
            
            for item_data in items_data:
                product = Product.objects.get(id=item_data['product_id'])
                quantity = item_data['quantity']
                
                if product.stock < quantity:
                    return Response({'error': f'Insufficient stock for {product.name}'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                
                if seller is None:
                    seller = product.user
                elif seller != product.user:
                    return Response({'error': 'All items must be from the same seller'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                
                total_amount += product.price * quantity
                products_to_update.append((product, quantity))
            
            # Create order
            order = Order.objects.create(
                buyer=request.user,
                seller=seller,
                total_amount=total_amount,
                notes=notes,
                status='pending'
            )
            
            # Create order items and update stock
            for item_data in items_data:
                product = Product.objects.get(id=item_data['product_id'])
                quantity = item_data['quantity']
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                
                product.stock -= quantity
                product.save()
            
            # Create notification for seller
            from notifications.views import create_notification
            create_notification(
                seller, 'order', 'New Order',
                f'You have a new order from {request.user.username}',
                order.id
            )
            
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Order.objects.filter(buyer=self.request.user)
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset.order_by('-created_at')


class SalesOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Order.objects.filter(seller=self.request.user)
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset.order_by('-created_at')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_details(request, orderId):
    try:
        order = Order.objects.get(
            id=orderId
        )
        if order.buyer != request.user and order.seller != request.user:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def accept_order(request, orderId):
    try:
        order = Order.objects.get(id=orderId, seller=request.user)
        if order.status == 'pending':
            order.accept_order()
            return Response({'status': 'Order accepted'})
        return Response({'error': 'Order cannot be accepted'}, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reject_order(request, orderId):
    try:
        order = Order.objects.get(id=orderId, seller=request.user)
        reason = request.data.get('reason', '')
        
        if order.status == 'pending':
            order.reject_order(reason)
            return Response({'status': 'Order rejected'})
        return Response({'error': 'Order cannot be rejected'}, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def complete_order(request, orderId):
    try:
        order = Order.objects.get(id=orderId)
        if order.buyer != request.user and order.seller != request.user:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if order.status == 'accepted':
            order.complete_order()
            return Response({'status': 'Order completed'})
        return Response({'error': 'Order cannot be completed'}, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
