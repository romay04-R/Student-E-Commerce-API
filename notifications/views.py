from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)
        unread_only = self.request.query_params.get('unread_only', 'false').lower() == 'true'
        if unread_only:
            queryset = queryset.filter(is_read=False)
        return queryset.order_by('-created_at')


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notificationId):
    try:
        notification = Notification.objects.get(id=notificationId, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({'status': 'Notification marked as read'})
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return Response({'status': 'All notifications marked as read'})


def create_notification(user, type, title, message, related_object_id=None):
    """Helper function to create notifications"""
    return Notification.objects.create(
        user=user,
        type=type,
        title=title,
        message=message,
        related_object_id=related_object_id
    )
