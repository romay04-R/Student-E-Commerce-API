from django.urls import path
from .views import NotificationListView, mark_notification_read, mark_all_notifications_read

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:notificationId>/read/', mark_notification_read, name='mark-notification-read'),
    path('mark-all-read/', mark_all_notifications_read, name='mark-all-read'),
]
