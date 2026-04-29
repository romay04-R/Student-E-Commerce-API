from django.urls import path, include
from .views import (
    OrderViewSet, create_order, PurchaseOrdersView, SalesOrdersView,
    get_order_details, accept_order, reject_order, complete_order
)
from .payment_views import initialize_payment, verify_payment, paystack_webhook
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('create/', create_order, name='create-order'),
    path('purchases/', PurchaseOrdersView.as_view(), name='purchase-orders'),
    path('sales/', SalesOrdersView.as_view(), name='sales-orders'),
    path('details/<int:orderId>/', get_order_details, name='order-details'),
    path('<int:orderId>/accept/', accept_order, name='accept-order'),
    path('<int:orderId>/reject/', reject_order, name='reject-order'),
    path('<int:orderId>/complete/', complete_order, name='complete-order'),
    # Payment URLs
    path('payment/initialize/', initialize_payment, name='initialize-payment'),
    path('payment/verify/', verify_payment, name='verify-payment'),
    path('payment/webhook/', paystack_webhook, name='paystack-webhook'),
]
