from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from .models import ChatMessage, ChatRoom
from orders.models import Order
from users.models import Cafeteria

User = get_user_model()


class ChatTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create test users
        self.student = User.objects.create_user(
            username='student1',
            email='student@test.com',
            password='testpass123',
            user_type='student'
        )
        
        self.vendor = User.objects.create_user(
            username='vendor1',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        self.delivery_person = User.objects.create_user(
            username='delivery1',
            email='delivery@test.com',
            password='testpass123',
            user_type='delivery'
        )
        
        # Create cafeteria
        self.cafeteria = Cafeteria.objects.create(
            name='Test Cafeteria',
            vendor=self.vendor,
            location='Campus Center',
            phone_number='1234567890',
            opening_time='08:00:00',
            closing_time='20:00:00'
        )
        
        # Create test order
        self.order = Order.objects.create(
            student=self.student,
            vendor=self.vendor,
            total_amount=Decimal('5.99'),
            delivery_address='Test Address',
            estimated_preparation_time=15
        )

    def test_student_can_send_message_to_vendor(self):
        """Test that students can send messages to vendors"""
        self.client.force_authenticate(user=self.student)
        
        message_data = {
            'receiver': self.vendor.id,
            'order': self.order.id,
            'message': 'When will my order be ready?'
        }
        
        response = self.client.post('/api/chat/send/', message_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify message was created
        message = ChatMessage.objects.get(id=response.data['message']['id'])
        self.assertEqual(message.sender, self.student)
        self.assertEqual(message.receiver, self.vendor)
        self.assertEqual(message.order, self.order)

    def test_vendor_can_reply_to_student(self):
        """Test that vendors can reply to students"""
        self.client.force_authenticate(user=self.vendor)
        
        message_data = {
            'receiver': self.student.id,
            'order': self.order.id,
            'message': 'Your order will be ready in 10 minutes'
        }
        
        response = self.client.post('/api/chat/send/', message_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_view_order_chat_messages(self):
        """Test viewing chat messages for an order"""
        # Clear any existing messages for this order first
        ChatMessage.objects.filter(order=self.order).delete()
        
        # Create some messages
        ChatMessage.objects.create(
            sender=self.student,
            receiver=self.vendor,
            order=self.order,
            message='Test message 1'
        )
        ChatMessage.objects.create(
            sender=self.vendor,
            receiver=self.student,
            order=self.order,
            message='Test reply 1'
        )
        
        self.client.force_authenticate(user=self.student)
        response = self.client.get(f'/api/chat/orders/{self.order.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_unauthorized_users_cannot_access_chat(self):
        """Test that unauthorized users cannot access order chat"""
        # Create another user not involved in the order
        other_user = User.objects.create_user(
            username='other',
            email='other@test.com',
            password='testpass123',
            user_type='student'
        )
        
        self.client.force_authenticate(user=other_user)
        response = self.client.get(f'/api/chat/orders/{self.order.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_chat_room_creation(self):
        """Test that chat rooms are created automatically"""
        self.client.force_authenticate(user=self.student)
        
        message_data = {
            'receiver': self.vendor.id,
            'order': self.order.id,
            'message': 'Test message'
        }
        
        response = self.client.post('/api/chat/send/', message_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify chat room was created
        chat_room = ChatRoom.objects.get(order=self.order)
        self.assertIn(self.student, chat_room.participants.all())
        self.assertIn(self.vendor, chat_room.participants.all())

    def test_unread_messages_count(self):
        """Test unread messages count endpoint"""
        # Create unread message
        ChatMessage.objects.create(
            sender=self.vendor,
            receiver=self.student,
            order=self.order,
            message='Unread message',
            is_read=False
        )
        
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/chat/unread-count/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 1)
