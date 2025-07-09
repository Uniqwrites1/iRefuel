from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import ChatMessage, ChatRoom
from .serializers import ChatMessageSerializer, ChatMessageCreateSerializer, ChatRoomSerializer
from orders.models import Order

User = get_user_model()


class OrderChatMessagesView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        order = get_object_or_404(Order, id=order_id)
        user = self.request.user
        
        # Check if user is involved in the order
        involved_users = [order.student, order.vendor]
        if order.delivery_person:
            involved_users.append(order.delivery_person)
        
        if user not in involved_users:
            raise PermissionDenied("You are not involved in this order.")
        
        # Mark messages as read for the current user
        ChatMessage.objects.filter(
            order=order,
            receiver=user,
            is_read=False
        ).update(is_read=True)
        
        return ChatMessage.objects.filter(order=order)


class SendMessageView(generics.CreateAPIView):
    serializer_class = ChatMessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        
        # Create or get chat room for the order
        order = message.order
        chat_room, created = ChatRoom.objects.get_or_create(order=order)
        
        if created:
            # Add all involved users to the chat room
            participants = [order.student, order.vendor]
            if order.delivery_person:
                participants.append(order.delivery_person)
            chat_room.participants.set(participants)
        
        return Response({
            'message': ChatMessageSerializer(message).data,
            'chat_room': ChatRoomSerializer(chat_room).data
        }, status=status.HTTP_201_CREATED)


class UserChatRoomsView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(
            participants=self.request.user,
            is_active=True
        ).order_by('-created_at')


class UnreadMessagesCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        unread_count = ChatMessage.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
        
        return Response({'unread_count': unread_count})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_order_participants(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user = request.user
    
    # Check if user is involved in the order
    involved_users = [order.student, order.vendor]
    if order.delivery_person:
        involved_users.append(order.delivery_person)
    
    if user not in involved_users:
        raise PermissionDenied("You are not involved in this order.")
    
    participants = []
    for participant in involved_users:
        if participant != user:  # Exclude the current user
            participants.append({
                'id': participant.id,
                'name': participant.get_full_name(),
                'user_type': participant.user_type,
                'username': participant.username
            })
    
    return Response({
        'order_id': order.id,
        'participants': participants
    })
