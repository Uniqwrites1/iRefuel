from django.db import models
from django.contrib.auth import get_user_model
from orders.models import Order

User = get_user_model()


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} - Order #{self.order.id}"


class ChatRoom(models.Model):
    """Chat room for an order involving student, vendor, and delivery person"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='chat_room')
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Chat Room for Order #{self.order.id}"
