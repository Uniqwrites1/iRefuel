from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Cafeteria, MenuItem

User = get_user_model()


class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('users:signup')
        self.login_url = reverse('users:login')

    def test_user_registration(self):
        """Test user registration for different user types"""
        user_data = {
            'username': 'teststudent',
            'email': 'student@test.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'Student',
            'user_type': 'student',
            'phone_number': '1234567890',
            'campus_location': 'North Campus'
        }
        
        response = self.client.post(self.signup_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        # Check user was created
        user = User.objects.get(username='teststudent')
        self.assertEqual(user.user_type, 'student')
        self.assertEqual(user.email, 'student@test.com')

    def test_user_login(self):
        """Test user login with JWT tokens"""
        # Create user first
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            user_type='student'
        )
        
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login(self):
        """Test login with incorrect credentials"""
        login_data = {
            'username': 'nonexistent',
            'password': 'wrongpass'
        }
        
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CafeteriaTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create vendor user
        self.vendor = User.objects.create_user(
            username='vendor1',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
        )
        
        # Create student user
        self.student = User.objects.create_user(
            username='student1',
            email='student@test.com',
            password='testpass123',
            user_type='student'
        )
        
        # Create cafeteria
        self.cafeteria = Cafeteria.objects.create(
            name='Test Cafeteria',
            description='A test cafeteria',
            vendor=self.vendor,
            location='Campus Center',
            phone_number='1234567890',
            opening_time='08:00:00',
            closing_time='20:00:00'
        )

    def test_student_can_view_cafeterias(self):
        """Test that students can view cafeterias"""
        self.client.force_authenticate(user=self.student)
        url = reverse('users:cafeteria-list')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Cafeteria')

    def test_vendor_can_manage_cafeteria(self):
        """Test that vendors can manage their cafeteria"""
        self.client.force_authenticate(user=self.vendor)
        url = reverse('users:vendor-cafeteria')
        
        # Get cafeteria
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Cafeteria')
        
        # Update cafeteria
        update_data = {'description': 'Updated description'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify update
        self.cafeteria.refresh_from_db()
        self.assertEqual(self.cafeteria.description, 'Updated description')


class MenuItemTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create vendor user
        self.vendor = User.objects.create_user(
            username='vendor1',
            email='vendor@test.com',
            password='testpass123',
            user_type='vendor'
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
        
        # Create menu item
        self.menu_item = MenuItem.objects.create(
            cafeteria=self.cafeteria,
            name='Test Burger',
            description='Delicious test burger',
            price=5.99,
            category='main_course',
            is_available=True,
            preparation_time=15
        )

    def test_vendor_can_create_menu_item(self):
        """Test that vendors can create menu items"""
        self.client.force_authenticate(user=self.vendor)
        url = reverse('users:vendor-menu-items')
        
        menu_item_data = {
            'name': 'New Pizza',
            'description': 'Delicious pizza',
            'price': 12.99,
            'category': 'main_course',
            'is_available': True,
            'preparation_time': 20
        }
        
        response = self.client.post(url, menu_item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 2)

    def test_vendor_can_update_menu_item(self):
        """Test that vendors can update their menu items"""
        self.client.force_authenticate(user=self.vendor)
        url = reverse('users:vendor-menu-item-detail', kwargs={'pk': self.menu_item.id})
        
        update_data = {'price': 6.99, 'is_available': False}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify update
        self.menu_item.refresh_from_db()
        self.assertEqual(float(self.menu_item.price), 6.99)
        self.assertFalse(self.menu_item.is_available)
