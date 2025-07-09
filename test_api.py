#!/usr/bin/env python
"""
Comprehensive API Testing Script for University Vendor App
"""
import requests
import json
import sys
from datetime import datetime

# Base URL for the API
BASE_URL = 'http://localhost:8000/api'

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.tokens = {}
        self.test_data = {}
        
    def print_result(self, test_name, success, details=None):
        """Print test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details and not success:
            print(f"   Details: {details}")
        print()
    
    def test_user_registration_and_login(self):
        """Test user registration and login for all user types"""
        print("🔐 Testing User Authentication...")
        
        # Test data for different user types
        users_data = [
            {
                'username': 'teststudent',
                'email': 'student@test.com',
                'password': 'testpass123',
                'password_confirm': 'testpass123',
                'first_name': 'Test',
                'last_name': 'Student',
                'user_type': 'student',
                'phone_number': '1234567890',
                'campus_location': 'North Campus'
            },
            {
                'username': 'testvendor',
                'email': 'vendor@test.com',
                'password': 'testpass123',
                'password_confirm': 'testpass123',
                'first_name': 'Test',
                'last_name': 'Vendor',
                'user_type': 'vendor',
                'phone_number': '1234567891',
                'campus_location': 'Campus Center'
            },
            {
                'username': 'testdelivery',
                'email': 'delivery@test.com',
                'password': 'testpass123',
                'password_confirm': 'testpass123',
                'first_name': 'Test',
                'last_name': 'Delivery',
                'user_type': 'delivery',
                'phone_number': '1234567892',
                'campus_location': 'South Campus'
            }
        ]
        
        # Test registration
        for user_data in users_data:
            try:
                response = self.session.post(f'{self.base_url}/users/signup/', json=user_data)
                success = response.status_code == 201
                
                if success:
                    data = response.json()
                    self.tokens[user_data['user_type']] = {
                        'access': data['access'],
                        'refresh': data['refresh'],
                        'user_id': data['user']['id']
                    }
                    self.test_data[f"{user_data['user_type']}_user"] = data['user']
                
                self.print_result(
                    f"Register {user_data['user_type']} user", 
                    success, 
                    response.text if not success else None
                )
                
            except Exception as e:
                self.print_result(f"Register {user_data['user_type']} user", False, str(e))
        
        # Test login
        for user_data in users_data:
            try:
                login_data = {
                    'username': user_data['username'],
                    'password': user_data['password']
                }
                response = self.session.post(f'{self.base_url}/users/login/', json=login_data)
                success = response.status_code == 200
                
                self.print_result(
                    f"Login {user_data['user_type']} user", 
                    success, 
                    response.text if not success else None
                )
                
            except Exception as e:
                self.print_result(f"Login {user_data['user_type']} user", False, str(e))
    
    def test_cafeteria_and_menu_management(self):
        """Test cafeteria and menu item management"""
        print("🏪 Testing Cafeteria & Menu Management...")
        
        if 'vendor' not in self.tokens:
            self.print_result("Cafeteria tests", False, "No vendor token available")
            return
        
        # Set vendor authentication
        headers = {'Authorization': f"Bearer {self.tokens['vendor']['access']}"}
        
        # Create cafeteria (assuming vendor needs to create/update their cafeteria)
        cafeteria_data = {
            'name': 'Test Cafeteria',
            'description': 'A test cafeteria for API testing',
            'location': 'Campus Center',
            'phone_number': '1234567890',
            'opening_time': '08:00:00',
            'closing_time': '20:00:00'
        }
        
        try:
            # Try to get existing cafeteria first
            response = self.session.get(f'{self.base_url}/users/vendor/cafeteria/', headers=headers)
            if response.status_code == 404:
                # Create new cafeteria if needed
                pass
            
            self.print_result("Get vendor cafeteria", response.status_code in [200, 404])
            
        except Exception as e:
            self.print_result("Get vendor cafeteria", False, str(e))
        
        # Test menu item creation
        menu_items_data = [
            {
                'name': 'Test Burger',
                'description': 'Delicious test burger',
                'price': '8.99',
                'category': 'main_course',
                'is_available': True,
                'preparation_time': 15
            },
            {
                'name': 'Test Fries',
                'description': 'Crispy test fries',
                'price': '3.99',
                'category': 'side',
                'is_available': True,
                'preparation_time': 10
            }
        ]
        
        for item_data in menu_items_data:
            try:
                response = self.session.post(
                    f'{self.base_url}/users/vendor/menu-items/', 
                    json=item_data, 
                    headers=headers
                )
                success = response.status_code == 201
                
                if success:
                    item = response.json()
                    self.test_data[f"menu_item_{item_data['category']}"] = item
                
                self.print_result(
                    f"Create menu item: {item_data['name']}", 
                    success, 
                    response.text if not success else None
                )
                
            except Exception as e:
                self.print_result(f"Create menu item: {item_data['name']}", False, str(e))
    
    def test_order_placement_and_management(self):
        """Test order placement and management workflow"""
        print("📦 Testing Order Management...")
        
        if 'student' not in self.tokens or 'vendor' not in self.tokens:
            self.print_result("Order tests", False, "Missing user tokens")
            return
        
        # Student places order
        student_headers = {'Authorization': f"Bearer {self.tokens['student']['access']}"}
        vendor_headers = {'Authorization': f"Bearer {self.tokens['vendor']['access']}"}
        
        # First, get available cafeterias
        try:
            response = self.session.get(f'{self.base_url}/users/cafeterias/', headers=student_headers)
            success = response.status_code == 200
            
            if success:
                cafeterias = response.json()
                self.print_result("Get cafeterias list", success)
                
                if cafeterias:
                    cafeteria = cafeterias[0]
                    self.test_data['cafeteria'] = cafeteria
                    
                    # Get menu for this cafeteria
                    menu_response = self.session.get(
                        f"{self.base_url}/users/cafeterias/{cafeteria['id']}/menu/", 
                        headers=student_headers
                    )
                    
                    if menu_response.status_code == 200:
                        menu_items = menu_response.json()
                        self.print_result("Get cafeteria menu", True)
                        
                        if menu_items:
                            # Place order
                            order_data = {
                                'vendor': self.tokens['vendor']['user_id'],
                                'delivery_address': 'North Campus Dorm Room 101',
                                'special_instructions': 'Please knock loudly',
                                'items': [
                                    {
                                        'menu_item': menu_items[0]['id'],
                                        'quantity': 2,
                                        'special_requests': 'Extra sauce'
                                    }
                                ]
                            }
                            
                            if len(menu_items) > 1:
                                order_data['items'].append({
                                    'menu_item': menu_items[1]['id'],
                                    'quantity': 1
                                })
                            
                            order_response = self.session.post(
                                f'{self.base_url}/orders/', 
                                json=order_data, 
                                headers=student_headers
                            )
                            
                            order_success = order_response.status_code == 201
                            self.print_result("Place order", order_success, order_response.text if not order_success else None)
                            
                            if order_success:
                                order = order_response.json()
                                self.test_data['order'] = order
                                
                                # Test order status update by vendor
                                status_update_data = {'status': 'confirmed'}
                                status_response = self.session.patch(
                                    f"{self.base_url}/orders/{order['id']}/status/",
                                    json=status_update_data,
                                    headers=vendor_headers
                                )
                                
                                self.print_result(
                                    "Vendor confirms order", 
                                    status_response.status_code == 200,
                                    status_response.text if status_response.status_code != 200 else None
                                )
                        else:
                            self.print_result("Get cafeteria menu", False, "No menu items found")
                    else:
                        self.print_result("Get cafeteria menu", False, menu_response.text)
                else:
                    self.print_result("Get cafeterias list", False, "No cafeterias found")
            else:
                self.print_result("Get cafeterias list", success, response.text)
                
        except Exception as e:
            self.print_result("Order placement workflow", False, str(e))
    
    def test_chat_system(self):
        """Test chat messaging system"""
        print("💬 Testing Chat System...")
        
        if 'student' not in self.tokens or 'vendor' not in self.tokens or 'order' not in self.test_data:
            self.print_result("Chat tests", False, "Missing prerequisites")
            return
        
        student_headers = {'Authorization': f"Bearer {self.tokens['student']['access']}"}
        vendor_headers = {'Authorization': f"Bearer {self.tokens['vendor']['access']}"}
        
        order_id = self.test_data['order']['id']
        
        # Student sends message to vendor
        try:
            message_data = {
                'receiver': self.tokens['vendor']['user_id'],
                'order': order_id,
                'message': 'When will my order be ready?'
            }
            
            response = self.session.post(
                f'{self.base_url}/chat/send/', 
                json=message_data, 
                headers=student_headers
            )
            
            success = response.status_code == 201
            self.print_result("Student sends message", success, response.text if not success else None)
            
            # Vendor replies
            if success:
                reply_data = {
                    'receiver': self.tokens['student']['user_id'],
                    'order': order_id,
                    'message': 'Your order will be ready in 10 minutes!'
                }
                
                reply_response = self.session.post(
                    f'{self.base_url}/chat/send/', 
                    json=reply_data, 
                    headers=vendor_headers
                )
                
                self.print_result(
                    "Vendor replies", 
                    reply_response.status_code == 201,
                    reply_response.text if reply_response.status_code != 201 else None
                )
                
                # Get chat messages
                chat_response = self.session.get(
                    f'{self.base_url}/chat/orders/{order_id}/', 
                    headers=student_headers
                )
                
                self.print_result(
                    "Get chat messages", 
                    chat_response.status_code == 200,
                    chat_response.text if chat_response.status_code != 200 else None
                )
                
        except Exception as e:
            self.print_result("Chat system", False, str(e))
    
    def test_delivery_system(self):
        """Test delivery management system"""
        print("🚚 Testing Delivery System...")
        
        if 'delivery' not in self.tokens:
            self.print_result("Delivery tests", False, "No delivery person token")
            return
        
        delivery_headers = {'Authorization': f"Bearer {self.tokens['delivery']['access']}"}
        
        # Test delivery person location setup
        try:
            location_data = {
                'campus_area': 'North Campus',
                'is_available': True,
                'max_orders': 3
            }
            
            # Try to get existing location info
            location_response = self.session.get(
                f'{self.base_url}/delivery/location/', 
                headers=delivery_headers
            )
            
            if location_response.status_code == 404:
                # Create location info if it doesn't exist
                # This might need to be handled differently based on your implementation
                pass
            
            self.print_result(
                "Get delivery location info", 
                location_response.status_code in [200, 404]
            )
            
            # Test availability toggle
            toggle_response = self.session.patch(
                f'{self.base_url}/delivery/availability/toggle/', 
                headers=delivery_headers
            )
            
            self.print_result(
                "Toggle delivery availability", 
                toggle_response.status_code == 200,
                toggle_response.text if toggle_response.status_code != 200 else None
            )
            
            # Test viewing available deliveries
            available_response = self.session.get(
                f'{self.base_url}/delivery/requests/available/', 
                headers=delivery_headers
            )
            
            self.print_result(
                "Get available deliveries", 
                available_response.status_code == 200,
                available_response.text if available_response.status_code != 200 else None
            )
            
        except Exception as e:
            self.print_result("Delivery system", False, str(e))
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting University Vendor App API Tests")
        print("=" * 50)
        
        start_time = datetime.now()
        
        # Run all test suites
        self.test_user_registration_and_login()
        self.test_cafeteria_and_menu_management()
        self.test_order_placement_and_management()
        self.test_chat_system()
        self.test_delivery_system()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("=" * 50)
        print(f"✅ All tests completed in {duration:.2f} seconds")
        print(f"🕒 Test run completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """Main script to run API tests"""
    print("University Vendor App - API Test Suite")
    print("Make sure the Django development server is running on http://localhost:8000")
    
    # Check if server is running
    try:
        response = requests.get(f'{BASE_URL}/users/cafeterias/', timeout=5)
        print("✅ Server is accessible")
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to server. Please start Django development server.")
        print("Run: python manage.py runserver")
        sys.exit(1)
    
    # Run tests
    tester = APITester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
