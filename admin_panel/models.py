from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class ReportedUser(models.Model):
    STATUS_CHOICES = [
        ('under-review', 'Under Review'),
        ('suspended', 'Suspended'),
        ('cleared', 'Cleared'),
    ]
    
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reports')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='under-review')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Report against {self.reported_user.username}"


class ReportedProduct(models.Model):
    STATUS_CHOICES = [
        ('under-review', 'Under Review'),
        ('removed', 'Removed'),
        ('cleared', 'Cleared'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reports')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='under-review')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Report against product: {self.product.name}"
