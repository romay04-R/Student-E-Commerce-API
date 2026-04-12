from django.urls import path
from .views import (
    get_statistics, PendingProductsListView, approve_product, reject_product,
    ReportedUsersListView, ReportedProductsListView, suspend_user, remove_product,
    unsuspend_user, AdminUsersListView, report_product, report_user
)

urlpatterns = [
    path('statistics/', get_statistics, name='admin-statistics'),
    path('pending-products/', PendingProductsListView.as_view(), name='pending-products'),
    path('products/<int:productId>/approve/', approve_product, name='approve-product'),
    path('products/<int:productId>/reject/', reject_product, name='reject-product'),
    path('products/<int:productId>/', remove_product, name='remove-product'),
    path('products/<int:productId>/report/', report_product, name='report-product'),
    path('reported-users/', ReportedUsersListView.as_view(), name='reported-users'),
    path('reported-products/', ReportedProductsListView.as_view(), name='reported-products'),
    path('users/<int:userId>/suspend/', suspend_user, name='suspend-user'),
    path('users/<int:userId>/unsuspend/', unsuspend_user, name='unsuspend-user'),
    path('users/<int:userId>/report/', report_user, name='report-user'),
    path('users/', AdminUsersListView.as_view(), name='admin-users'),
]
