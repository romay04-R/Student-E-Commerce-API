from django.urls import path, include
from .views import (
    OrderViewSet, create_order, PurchaseOrdersView, SalesOrdersView,
    get_order_details, accept_order, reject_order, complete_order
)
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
]
