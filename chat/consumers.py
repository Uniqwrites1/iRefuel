import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage, ChatRoom
from orders.models import Order

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'chat_order_{self.order_id}'
        self.user = self.scope['user']

        # Check if user has permission to join this chat
        if await self.has_permission():
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_id = text_data_json['receiver_id']

        # Save message to database
        chat_message = await self.save_message(message, receiver_id)

        if chat_message:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': self.user.id,
                    'sender_name': self.user.get_full_name(),
                    'sender_type': self.user.user_type,
                    'receiver_id': receiver_id,
                    'timestamp': chat_message.timestamp.isoformat(),
                    'message_id': chat_message.id
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'sender_type': event['sender_type'],
            'receiver_id': event['receiver_id'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id']
        }))

    @database_sync_to_async
    def has_permission(self):
        """Check if user is involved in this order"""
        try:
            order = Order.objects.get(id=self.order_id)
            involved_users = [order.student, order.vendor]
            if order.delivery_person:
                involved_users.append(order.delivery_person)
            return self.user in involved_users
        except Order.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, message, receiver_id):
        """Save chat message to database"""
        try:
            order = Order.objects.get(id=self.order_id)
            receiver = User.objects.get(id=receiver_id)
            
            # Verify receiver is involved in the order
            involved_users = [order.student, order.vendor]
            if order.delivery_person:
                involved_users.append(order.delivery_person)
            
            if receiver not in involved_users or self.user not in involved_users:
                return None

            chat_message = ChatMessage.objects.create(
                sender=self.user,
                receiver=receiver,
                order=order,
                message=message
            )

            # Create or update chat room
            chat_room, created = ChatRoom.objects.get_or_create(order=order)
            if created:
                chat_room.participants.set(involved_users)

            return chat_message
        except (Order.DoesNotExist, User.DoesNotExist):
            return None


class NotificationConsumer(AsyncWebsocketConsumer):
    """Consumer for real-time notifications"""
    
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.user_group_name = f'user_{self.user.id}'
            
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )

    async def order_update(self, event):
        """Send order status updates"""
        await self.send(text_data=json.dumps({
            'type': 'order_update',
            'order_id': event['order_id'],
            'status': event['status'],
            'message': event['message']
        }))

    async def new_message(self, event):
        """Send new message notifications"""
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'order_id': event['order_id'],
            'sender_name': event['sender_name'],
            'message': event['message']
        }))

    async def delivery_request(self, event):
        """Send delivery assignment notifications"""
        await self.send(text_data=json.dumps({
            'type': 'delivery_request',
            'order_id': event['order_id'],
            'location': event['location'],
            'amount': event['amount']
        }))
