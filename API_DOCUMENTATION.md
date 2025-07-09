# University Vendor App - API Documentation

## Base URL
- **Development**: `http://localhost:8000/api/`
- **Production**: `https://your-domain.com/api/`

## Authentication
All endpoints (except registration and login) require JWT authentication.

### Headers Required
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

## Authentication Endpoints

### 1. User Registration
- **POST** `/users/register/`
- **Body**:
```json
{
  "username": "john_doe",
  "email": "john@university.edu",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "student",  // "student", "vendor", "delivery"
  "phone_number": "+1234567890",
  "campus_location": "North Campus"
}
```
- **Response** (201):
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@university.edu",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "student",
    "phone_number": "+1234567890",
    "campus_location": "North Campus",
    "profile_picture": null,
    "is_available": true,
    "created_at": "2025-06-26T10:00:00Z"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. User Login
- **POST** `/users/login/`
- **Body**:
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```
- **Response** (200):
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@university.edu",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "student",
    "phone_number": "+1234567890",
    "campus_location": "North Campus",
    "profile_picture": null,
    "is_available": true,
    "created_at": "2025-06-26T10:00:00Z"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Token Refresh
- **POST** `/token/refresh/`
- **Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
- **Response** (200):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## User Management Endpoints

### 4. Get User Profile
- **GET** `/users/profile/`
- **Response** (200):
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@university.edu",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "student",
  "phone_number": "+1234567890",
  "campus_location": "North Campus",
  "profile_picture": null,
  "is_available": true,
  "created_at": "2025-06-26T10:00:00Z"
}
```

### 5. Update User Profile
- **PATCH** `/users/profile/`
- **Body** (partial update):
```json
{
  "first_name": "John Updated",
  "phone_number": "+9876543210",
  "campus_location": "South Campus"
}
```

## Cafeteria & Menu Endpoints

### 6. List All Cafeterias (Students)
- **GET** `/users/cafeterias/`
- **Response** (200):
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "vendor": 2,
      "vendor_name": "Pizza Palace",
      "name": "Main Campus Pizza",
      "description": "Best pizza on campus",
      "location": "Student Union Building",
      "phone_number": "+1234567890",
      "email": "pizza@university.edu",
      "opening_time": "08:00:00",
      "closing_time": "22:00:00",
      "is_active": true,
      "image": null,
      "rating": "4.50",
      "created_at": "2025-06-26T10:00:00Z"
    }
  ]
}
```

### 7. Get Cafeteria Menu
- **GET** `/users/cafeterias/{cafeteria_id}/menu/`
- **Response** (200):
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Margherita Pizza",
      "price": "12.99",
      "category": "main_course",
      "image": null,
      "is_available": true,
      "preparation_time": 15
    }
  ]
}
```

### 8. Get Vendor's Cafeteria (Vendors only)
- **GET** `/users/vendor/cafeteria/`
- **Response** (200):
```json
{
  "id": 1,
  "vendor": 2,
  "vendor_name": "Pizza Palace",
  "name": "Main Campus Pizza",
  "description": "Best pizza on campus",
  "location": "Student Union Building",
  "phone_number": "+1234567890",
  "email": "pizza@university.edu",
  "opening_time": "08:00:00",
  "closing_time": "22:00:00",
  "is_active": true,
  "image": null,
  "rating": "4.50",
  "created_at": "2025-06-26T10:00:00Z"
}
```

### 9. Vendor Menu Items Management
- **GET** `/users/vendor/menu-items/` - List vendor's menu items
- **POST** `/users/vendor/menu-items/` - Create new menu item
- **Body** for POST:
```json
{
  "name": "Pepperoni Pizza",
  "description": "Classic pepperoni pizza",
  "price": "14.99",
  "category": "main_course",
  "is_available": true,
  "preparation_time": 20
}
```

### 10. Update/Delete Menu Item (Vendors only)
- **GET** `/users/vendor/menu-items/{item_id}/` - Get specific item
- **PATCH** `/users/vendor/menu-items/{item_id}/` - Update item
- **DELETE** `/users/vendor/menu-items/{item_id}/` - Delete item

## Order Management Endpoints

### 11. Place Order (Students only)
- **POST** `/orders/`
- **Body**:
```json
{
  "vendor": 2,
  "delivery_address": "Dorm Room 301, Building A",
  "special_instructions": "Extra cheese, no olives",
  "items": [
    {
      "menu_item": 1,
      "quantity": 2,
      "special_requests": "Extra spicy"
    },
    {
      "menu_item": 3,
      "quantity": 1
    }
  ]
}
```
- **Response** (201):
```json
{
  "id": 1,
  "student": 1,
  "student_name": "John Doe",
  "vendor": 2,
  "vendor_name": "Pizza Palace",
  "delivery_person": null,
  "delivery_person_name": null,
  "status": "pending",
  "total_amount": "27.97",
  "delivery_address": "Dorm Room 301, Building A",
  "special_instructions": "Extra cheese, no olives",
  "estimated_preparation_time": 20,
  "estimated_delivery_time": null,
  "created_at": "2025-06-26T11:00:00Z",
  "updated_at": "2025-06-26T11:00:00Z",
  "confirmed_at": null,
  "delivered_at": null,
  "items": [
    {
      "id": 1,
      "menu_item": 1,
      "menu_item_name": "Margherita Pizza",
      "menu_item_price": "12.99",
      "quantity": 2,
      "unit_price": "12.99",
      "subtotal": "25.98",
      "special_requests": "Extra spicy"
    }
  ]
}
```

### 12. Get Student Orders
- **GET** `/orders/student/`
- **Response**: Paginated list of student's orders

### 13. Get Vendor Orders
- **GET** `/orders/vendor/`
- **Response**: Paginated list of vendor's orders

### 14. Get Delivery Orders
- **GET** `/orders/delivery/`
- **Response**: Paginated list of available/assigned delivery orders

### 15. Update Order Status (Vendors only)
- **PATCH** `/orders/{order_id}/status/`
- **Body**:
```json
{
  "status": "confirmed",  // "confirmed", "preparing", "ready", "delivered", "cancelled"
  "estimated_delivery_time": "2025-06-26T12:30:00Z"
}
```

### 16. Get Delivery Locations
- **GET** `/orders/delivery-locations/`
- **Response** (200):
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "North Campus Dorms",
      "address": "123 University Ave",
      "latitude": "40.7128",
      "longitude": "-74.0060"
    }
  ]
}
```

## Chat Endpoints

### 17. Send Message
- **POST** `/chat/send/`
- **Body**:
```json
{
  "receiver": 2,
  "order": 1,
  "message": "When will my order be ready?"
}
```
- **Response** (201):
```json
{
  "success": true,
  "message": {
    "id": 1,
    "sender": 1,
    "sender_name": "John Doe",
    "sender_type": "student",
    "receiver": 2,
    "order": 1,
    "message": "When will my order be ready?",
    "is_read": false,
    "timestamp": "2025-06-26T11:30:00Z"
  }
}
```

### 18. Get Order Chat Messages
- **GET** `/chat/orders/{order_id}/`
- **Response** (200):
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "sender": 1,
      "sender_name": "John Doe",
      "sender_type": "student",
      "receiver": 2,
      "order": 1,
      "message": "When will my order be ready?",
      "is_read": true,
      "timestamp": "2025-06-26T11:30:00Z"
    }
  ]
}
```

### 19. Mark Messages as Read
- **POST** `/chat/orders/{order_id}/mark-read/`
- **Response** (200):
```json
{
  "success": true,
  "message": "Messages marked as read"
}
```

## Delivery Endpoints

### 20. Get Delivery Requests (Delivery Personnel)
- **GET** `/delivery/requests/`
- **Response**: Paginated list of delivery requests

### 21. Accept Delivery Request
- **POST** `/delivery/requests/{request_id}/accept/`
- **Response** (200):
```json
{
  "success": true,
  "message": "Delivery request accepted"
}
```

### 22. Update Delivery Status
- **PATCH** `/delivery/requests/{request_id}/status/`
- **Body**:
```json
{
  "status": "picked_up"  // "assigned", "picked_up", "delivered"
}
```

### 23. Toggle Delivery Availability
- **POST** `/delivery/toggle-availability/`
- **Response** (200):
```json
{
  "success": true,
  "is_available": false,
  "message": "Availability updated"
}
```

### 24. Update Delivery Location
- **POST** `/delivery/update-location/`
- **Body**:
```json
{
  "latitude": "40.7128",
  "longitude": "-74.0060"
}
```

## WebSocket Endpoints (Real-time Chat)

### Chat WebSocket
- **URL**: `ws://localhost:8000/ws/chat/orders/{order_id}/`
- **Authentication**: Include JWT token in connection headers
- **Message Format**:
```json
{
  "type": "chat_message",
  "message": "Hello!",
  "receiver_id": 2
}
```

## Error Responses

All endpoints return consistent error responses:

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "A server error occurred."
}
```

## Data Models

### User Types
- `student`: Can place orders, chat with vendors/delivery
- `vendor`: Can manage cafeteria, menu items, view orders
- `delivery`: Can accept delivery requests, update delivery status

### Order Status Flow
1. `pending` → `confirmed` → `preparing` → `ready` → `delivered`
2. Can be `cancelled` at any stage before `ready`

### Menu Item Categories
- `appetizer`
- `main_course`
- `dessert`
- `beverage`
- `snack`

### Delivery Status Flow
1. `assigned` → `picked_up` → `delivered`

## Rate Limiting
- Authentication endpoints: 5 requests per minute
- Other endpoints: 100 requests per minute per user

## File Uploads
For image uploads (profile pictures, menu item images):
- Use `multipart/form-data` content type
- Maximum file size: 5MB
- Supported formats: JPG, PNG, WebP

## Testing
Use the provided test script at `/test_api.py` to test all endpoints.

## Support
For API support, contact the backend development team.
