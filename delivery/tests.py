from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import DeliveryRequest, DeliveryPersonLocation
from .services import DeliveryAssignmentService
from orders.models import Order
from users.models import Cafeteria

User = get_user_model()


class DeliveryTestCase(TestCase):
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
        
        # Create delivery person location
        self.delivery_location = DeliveryPersonLocation.objects.create(
            delivery_person=self.delivery_person,
            campus_area='North Campus',
            is_available=True,
            current_orders_count=0,
            max_orders=3
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
            total_amount=Decimal('15.99'),
            delivery_address='North Campus Dorm A',
            status='ready_for_delivery',
            estimated_preparation_time=20
        )

    def test_delivery_person_can_view_available_deliveries(self):
        """Test that delivery personnel can view available deliveries"""
        self.client.force_authenticate(user=self.delivery_person)
        
        response = self.client.get('/api/delivery/requests/available/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delivery_person_can_accept_delivery(self):
        """Test that delivery personnel can accept deliveries"""
        self.client.force_authenticate(user=self.delivery_person)
        
        response = self.client.patch(f'/api/orders/{self.order.id}/accept-delivery/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify order was assigned
        self.order.refresh_from_db()
        self.assertEqual(self.order.delivery_person, self.delivery_person)

    def test_delivery_person_can_update_delivery_status(self):
        """Test that delivery personnel can update delivery status"""
        # Create delivery assignment
        delivery_request = DeliveryRequest.objects.create(
            order=self.order,
            delivery_person=self.delivery_person,
            status='accepted'
        )
        
        self.client.force_authenticate(user=self.delivery_person)
        
        response = self.client.patch(
            f'/api/delivery/requests/{delivery_request.id}/status/',
            {'status': 'picked_up'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        delivery_request.refresh_from_db()
        self.assertEqual(delivery_request.status, 'picked_up')

    def test_delivery_person_can_toggle_availability(self):
        """Test that delivery personnel can toggle availability"""
        self.client.force_authenticate(user=self.delivery_person)
        
        response = self.client.patch('/api/delivery/availability/toggle/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check availability was toggled
        self.delivery_location.refresh_from_db()
        self.assertFalse(self.delivery_location.is_available)

    def test_vendor_can_auto_assign_delivery(self):
        """Test that vendors can auto-assign delivery personnel"""
        self.client.force_authenticate(user=self.vendor)
        
        response = self.client.post(f'/api/delivery/auto-assign/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify delivery was assigned
        self.order.refresh_from_db()
        self.assertEqual(self.order.delivery_person, self.delivery_person)

    def test_delivery_statistics(self):
        """Test delivery statistics endpoint"""
        # Create some completed deliveries
        completed_order = Order.objects.create(
            student=self.student,
            vendor=self.vendor,
            delivery_person=self.delivery_person,
            total_amount=Decimal('10.99'),
            delivery_address='Test Address',
            status='delivered',
            estimated_preparation_time=15
        )
        
        DeliveryRequest.objects.create(
            order=completed_order,
            delivery_person=self.delivery_person,
            status='delivered'
        )
        
        self.client.force_authenticate(user=self.delivery_person)
        response = self.client.get('/api/delivery/statistics/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_delivered', response.data)
        self.assertIn('current_orders', response.data)
        self.assertIn('is_available', response.data)


class DeliveryAssignmentServiceTestCase(TestCase):
    def setUp(self):
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
        
        self.delivery_person1 = User.objects.create_user(
            username='delivery1',
            email='delivery1@test.com',
            password='testpass123',
            user_type='delivery'
        )
        
        self.delivery_person2 = User.objects.create_user(
            username='delivery2',
            email='delivery2@test.com',
            password='testpass123',
            user_type='delivery'
        )
        
        # Create delivery person locations
        DeliveryPersonLocation.objects.create(
            delivery_person=self.delivery_person1,
            campus_area='North Campus',
            is_available=True,
            current_orders_count=1,
            max_orders=3
        )
        
        DeliveryPersonLocation.objects.create(
            delivery_person=self.delivery_person2,
            campus_area='North Campus',
            is_available=True,
            current_orders_count=0,
            max_orders=3
        )
        
        # Create test order
        self.order = Order.objects.create(
            student=self.student,
            vendor=self.vendor,
            total_amount=Decimal('15.99'),
            delivery_address='North Campus Dorm A',
            status='ready_for_delivery',
            estimated_preparation_time=20
        )

    def test_find_available_delivery_personnel(self):
        """Test finding available delivery staff"""
        available = DeliveryAssignmentService.find_available_delivery_personnel(self.order)
        self.assertEqual(len(available), 2)
        self.assertIn(self.delivery_person1, available)
        self.assertIn(self.delivery_person2, available)

    def test_assign_delivery_person_selects_least_busy(self):
        """Test that assignment selects the least busy delivery person"""
        delivery_request = DeliveryAssignmentService.assign_delivery_person(self.order)
        
        self.assertIsNotNone(delivery_request)
        # Should select delivery_person2 who has 0 current orders vs delivery_person1 with 1
        self.assertEqual(delivery_request.delivery_person, self.delivery_person2)

    def test_complete_delivery_updates_counters(self):
        """Test that completing delivery updates order counters"""
        # Create delivery assignment
        delivery_request = DeliveryRequest.objects.create(
            order=self.order,
            delivery_person=self.delivery_person1,
            status='picked_up'
        )
        
        # Complete delivery
        success = DeliveryAssignmentService.complete_delivery(delivery_request)
        
        self.assertTrue(success)
        
        # Check order status was updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'delivered')
        
        # Check delivery assignment status was updated
        delivery_request.refresh_from_db()
        self.assertEqual(delivery_request.status, 'delivered')
        
        # Check delivery person's current orders count was decreased
        location_info = self.delivery_person1.location_info
        location_info.refresh_from_db()
        self.assertEqual(location_info.current_orders_count, 0)
