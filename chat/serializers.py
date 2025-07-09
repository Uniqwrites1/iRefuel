from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatMessage, ChatRoom
from orders.models import Order

User = get_user_model()


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    sender_type = serializers.CharField(source='sender.user_type', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ('id', 'sender', 'sender_name', 'sender_type', 'receiver', 
                 'order', 'message', 'is_read', 'timestamp')
        read_only_fields = ('id', 'sender', 'timestamp')


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('receiver', 'order', 'message')

    def validate(self, attrs):
        order = attrs['order']
        sender = self.context['request'].user
        receiver = attrs['receiver']
        
        # Confirm that sender and receiver are involved in the order
        involved_users = [order.student, order.vendor]
        if order.delivery_person:
            involved_users.append(order.delivery_person)
        
        if sender not in involved_users:
            raise serializers.ValidationError("You are not involved in this order.")
        
        if receiver not in involved_users:
            raise serializers.ValidationError("Receiver is not involved in this order.")
        
        if sender == receiver:
            raise serializers.ValidationError("You cannot send a message to yourself.")
        
        return attrs

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class ChatRoomSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True, read_only=True)
    order_info = serializers.SerializerMethodField()
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ('id', 'order', 'order_info', 'participants', 'latest_message', 
                 'created_at', 'is_active')
        read_only_fields = ('id', 'created_at')

    def get_order_info(self, obj):
        return {
            'id': obj.order.id,
            'status': obj.order.status,
            'total_amount': obj.order.total_amount,
            'student_name': obj.order.student.get_full_name(),
            'vendor_name': obj.order.vendor.get_full_name(),
        }

    def get_latest_message(self, obj):
        latest = obj.order.chat_messages.first()
        if latest:
            return {
                'message': latest.message,
                'sender': latest.sender.get_full_name(),
                'timestamp': latest.timestamp
            }
        return None
