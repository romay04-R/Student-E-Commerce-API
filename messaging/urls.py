from django.urls import path
from .views import (
    ConversationListView, MessageListView, send_message, 
    mark_messages_read, delete_conversation, get_messages_with_user
)

urlpatterns = [
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
    path('conversations/<int:conversationId>/messages/', MessageListView.as_view(), name='message-list'),
    path('conversations/<int:conversationId>/mark-read/', mark_messages_read, name='mark-messages-read'),
    path('conversations/<int:conversationId>/', delete_conversation, name='delete-conversation'),
    path('messages/', send_message, name='send-message'),
    path('messages/user/<int:userId>/', get_messages_with_user, name='messages-with-user'),
]
