from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from .models import Order, OrderItem, DeliveryLocation
from users.models import Cafeteria, MenuItem

User = get_user_model()


class OrderTestCase(TestCase):
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
        
        # Create test cafeteria and menu items
        self.cafeteria = Cafeteria.objects.create(
            name='Test Cafeteria',
            vendor=self.vendor,
            location='Campus Center',
            phone_number='1234567890',
            opening_time='08:00:00',
            closing_time='20:00:00'
        )
        
        self.menu_item1 = MenuItem.objects.create(
            cafeteria=self.cafeteria,
            name='Burger',
            price=Decimal('5.99'),
            is_available=True,
            category='main_course',
            preparation_time=15
        )
        
        self.menu_item2 = MenuItem.objects.create(
            cafeteria=self.cafeteria,
            name='Fries',
            price=Decimal('2.99'),
            is_available=True,
            category='side',
            preparation_time=10
        )

    def test_student_can_place_order(self):
        """Test that students can place orders"""
        self.client.force_authenticate(user=self.student)
        
        order_data = {
            'vendor': self.vendor.id,
            'delivery_address': 'Dorm Room 101',
            'special_instructions': 'Extra sauce please',
            'items': [
                {
                    'menu_item': self.menu_item1.id,
                    'quantity': 2,
                    'special_requests': 'No onions'
                },
                {
                    'menu_item': self.menu_item2.id,
                    'quantity': 1
                }
            ]
        }
        
        response = self.client.post('/api/orders/', order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify order was created correctly
        order = Order.objects.get(id=response.data['id'])
        self.assertEqual(order.student, self.student)
        self.assertEqual(order.vendor, self.vendor)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total_amount, Decimal('14.97'))  # (5.99*2) + 2.99
        self.assertEqual(order.items.count(), 2)

    def test_vendor_can_view_orders(self):
        """Test that vendors can view their orders"""
        # Create test order
        order = Order.objects.create(
            student=self.student,
            vendor=self.vendor,
            total_amount=Decimal('5.99'),
            delivery_address='Test Address',
            estimated_preparation_time=15
        )
        
        self.client.force_authenticate(user=self.vendor)
        response = self.client.get('/api/orders/vendor/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], order.id)

    def test_vendor_can_update_order_status(self):
        """Test that vendors can update order status"""
        order = Order.objects.create(
            student=self.student,
            vendor=self.vendor,
            total_amount=Decimal('5.99'),
            delivery_address='Test Address',
            status='pending',
            estimated_preparation_time=15
        )
        
        self.client.force_authenticate(user=self.vendor)
        
        # Update to confirmed
        response = self.client.patch(
            f'/api/orders/{order.id}/status/',
            {'status': 'confirmed'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, 'confirmed')

    def test_order_status_validation(self):
        """Test order status change validation"""
        order = Order.objects.create(
            student=self.student,
            vendor=self.vendor,
            total_amount=Decimal('5.99'),
            delivery_address='Test Address',
            status='pending',
            estimated_preparation_time=15
        )
        
        self.client.force_authenticate(user=self.vendor)
        
        # Try incorrect status transition
        response = self.client.patch(
            f'/api/orders/{order.id}/status/',
            {'status': 'delivered'},  # Cannot go directly from pending to delivered
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delivery_person_can_accept_order(self):
        """Test that delivery personnel can accept orders"""
        order = Order.objects.create(
            student=self.student,
            vendor=self.vendor,
            total_amount=Decimal('5.99'),
            delivery_address='Test Address',
            status='ready_for_delivery',
            estimated_preparation_time=15
        )
        
        self.client.force_authenticate(user=self.delivery_person)
        
        response = self.client.patch(f'/api/orders/{order.id}/accept-delivery/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.delivery_person, self.delivery_person)


class DeliveryLocationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = User.objects.create_user(
            username='student1',
            email='student@test.com',
            password='testpass123',
            user_type='student'
        )

    def test_can_list_delivery_locations(self):
        """Test listing delivery locations"""
        DeliveryLocation.objects.create(
            name='North Campus',
            description='North campus dormitories'
        )
        DeliveryLocation.objects.create(
            name='South Campus',
            description='South campus facilities'
        )
        
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/orders/delivery-locations/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
