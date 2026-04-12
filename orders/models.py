from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_orders')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.buyer.username} buying from {self.seller.username}"
    
    def get_product(self):
        """Get the single product in this order"""
        item = self.items.first()
        return item.product if item else None
    
    def accept_order(self):
        if self.status == 'pending':
            self.status = 'accepted'
            self.save()
            
            # Update seller's total sales
            from users.models import UserProfile
            profile, created = UserProfile.objects.get_or_create(user=self.seller)
            profile.total_sales += self.total_amount
            profile.save()
            
            # Create notification
            from notifications.views import create_notification
            create_notification(
                self.buyer, 'order', 'Order Accepted',
                f'Your order for {self.get_product().name} has been accepted by {self.seller.username}',
                self.id
            )
    
    def reject_order(self, reason=''):
        if self.status == 'pending':
            self.status = 'rejected'
            self.save()
            
            # Restore product stock
            for item in self.items.all():
                item.product.stock += item.quantity
                item.product.save()
            
            # Create notification
            from notifications.views import create_notification
            create_notification(
                self.buyer, 'order', 'Order Rejected',
                f'Your order for {self.get_product().name} has been rejected. Reason: {reason}',
                self.id
            )
    
    def complete_order(self):
        if self.status == 'accepted':
            self.status = 'completed'
            self.save()
            
            # Create notifications for both parties
            from notifications.views import create_notification
            create_notification(
                self.buyer, 'order', 'Order Completed',
                f'Your order for {self.get_product().name} has been marked as completed',
                self.id
            )
            create_notification(
                self.seller, 'order', 'Order Completed',
                f'Order for {self.get_product().name} has been completed',
                self.id
            )
    
    def cancel_order(self, reason=''):
        if self.status == 'pending':
            self.status = 'cancelled'
            self.save()
            
            # Restore product stock
            for item in self.items.all():
                item.product.stock += item.quantity
                item.product.save()
            
            # Create notification for seller
            from notifications.views import create_notification
            create_notification(
                self.seller, 'order', 'Order Cancelled',
                f'Order for {self.get_product().name} has been cancelled by {self.buyer.username}. Reason: {reason}',
                self.id
            )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
