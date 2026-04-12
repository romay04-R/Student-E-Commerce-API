from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        conversation_id = self.kwargs['conversationId']
        return Message.objects.filter(conversation_id=conversation_id).order_by('created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_message(request):
    recipient_id = request.data.get('recipient_id')
    content = request.data.get('content')
    
    if not recipient_id or not content:
        return Response({'error': 'recipient_id and content are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create conversation
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(participants_id=recipient_id).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)
        conversation.participants.add_id(recipient_id)
    
    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        content=content
    )
    
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def mark_messages_read(request, conversationId):
    conversation = Conversation.objects.get(id=conversationId, participants=request.user)
    unread_messages = conversation.messages.filter(is_read=False).exclude(sender=request.user)
    unread_messages.update(is_read=True)
    
    return Response({'status': 'Messages marked as read'})


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_conversation(request, conversationId):
    conversation = Conversation.objects.get(id=conversationId, participants=request.user)
    conversation.delete()
    
    return Response({'status': 'Conversation deleted'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_messages_with_user(request, userId):
    # Get conversation between current user and specified user
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(participants_id=userId).first()
    
    if not conversation:
        return Response({'messages': []})
    
    messages = conversation.messages.order_by('created_at')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)
