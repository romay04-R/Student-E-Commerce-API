from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication & User Management
    path('api/auth/', include('users.urls')),
    path('api/users/', include('users.urls')),
    # Products
    path('api/products/', include('products.urls')),
    # Orders
    path('api/orders/', include('orders.urls')),
    # Messaging
    path('api/', include('messaging.urls')),
    # Notifications
    path('api/notifications/', include('notifications.urls')),
    # Admin Panel
    path('api/admin/', include('admin_panel.urls')),
    # System Endpoints
    path('api/', include('system.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
