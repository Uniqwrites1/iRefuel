# Frontend Integration Guide

## Overview
This guide provides all necessary information for integrating with the University Vendor App backend API.

## Getting Started

### 1. Base Configuration
```
Development URL: http://localhost:8000/api/
Production URL: https://your-domain.com/api/
```

### 2. Required Headers
```
Content-Type: application/json
Authorization: Bearer <access_token>  (for authenticated endpoints)
```

## Authentication Flow

### Step 1: User Registration
```
POST /api/users/register/
Body: {
  username, email, password, password_confirm, 
  first_name, last_name, user_type, phone_number, campus_location
}
Response: { user, refresh, access }
```

### Step 2: User Login
```
POST /api/users/login/
Body: { username, password }
Response: { user, refresh, access }
```

### Step 3: Token Management
- Store `access` token for API calls
- Store `refresh` token for token renewal
- Access tokens expire in 60 minutes
- Refresh tokens expire in 7 days

### Step 4: Token Refresh
```
POST /api/token/refresh/
Body: { refresh }
Response: { access }
```

## User Role-Based Features

### Students Can:
- Register/Login
- View all cafeterias and menus
- Place orders
- Chat with vendors and delivery personnel
- Track order status
- View order history

### Vendors Can:
- Register/Login
- Manage their cafeteria information
- Create/update/delete menu items
- View and manage incoming orders
- Update order status
- Chat with students and delivery personnel

### Delivery Personnel Can:
- Register/Login
- View available delivery requests
- Accept delivery assignments
- Update delivery status
- Update their location
- Toggle availability status
- Chat with students and vendors

## Key API Workflows

### 1. Student Order Flow
```
1. GET /api/users/cafeterias/ (browse cafeterias)
2. GET /api/users/cafeterias/{id}/menu/ (view menu)
3. POST /api/orders/ (place order)
4. GET /api/orders/student/ (track orders)
5. GET /api/chat/orders/{order_id}/ (chat about order)
```

### 2. Vendor Order Management Flow
```
1. GET /api/orders/vendor/ (view incoming orders)
2. PATCH /api/orders/{id}/status/ (update order status)
3. GET /api/chat/orders/{order_id}/ (communicate with customer)
```

### 3. Delivery Assignment Flow
```
1. GET /api/delivery/requests/ (view available deliveries)
2. POST /api/delivery/requests/{id}/accept/ (accept delivery)
3. PATCH /api/delivery/requests/{id}/status/ (update status)
4. POST /api/delivery/update-location/ (update location)
```

## Real-time Features

### WebSocket Chat
```
URL: ws://localhost:8000/ws/chat/orders/{order_id}/
Authentication: Include JWT token in connection headers
Message Format: {
  "type": "chat_message",
  "message": "Hello!",
  "receiver_id": 2
}
```

## Error Handling

### Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

### Error Response Format
```json
{
  "field_name": ["Error message"],
  "detail": "General error message"
}
```

## Data Validation

### Required Fields for Registration
- username (unique)
- email (valid email format)
- password (minimum 8 characters)
- password_confirm (must match password)
- user_type (student/vendor/delivery)

### Order Placement Requirements
- Valid vendor ID
- At least one menu item
- Valid delivery address
- Menu items must be available

### File Upload Constraints
- Maximum size: 5MB
- Supported formats: JPG, PNG, WebP
- Use multipart/form-data for uploads

## Pagination

All list endpoints return paginated responses:
```json
{
  "count": 25,
  "next": "http://api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

## Rate Limiting
- Authentication endpoints: 5 requests/minute
- Other endpoints: 100 requests/minute per user

## Security Considerations

### Development
- CORS is enabled for localhost:3000, localhost:8080
- Debug mode is enabled
- Uses SQLite database

### Production Recommendations
- Set DEBUG=False in .env
- Use strong SECRET_KEY
- Configure proper ALLOWED_HOSTS
- Use PostgreSQL database
- Enable HTTPS
- Set proper CORS origins
- Use Redis for better performance

## Testing

### Available Test Data
Use the test script at `/test_api.py` to:
- Create test users of all types
- Create sample cafeterias and menu items
- Place test orders
- Test chat functionality

### Sample Test Users
```
Student: username=test_student, password=testpass123
Vendor: username=test_vendor, password=testpass123
Delivery: username=test_delivery, password=testpass123
```

## Environment Variables

Key configuration in `.env`:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
USE_POSTGRES=False
JWT_ACCESS_TOKEN_LIFETIME=60
CORS_ALLOW_ALL_ORIGINS=True
```

## API Versioning
- Current version: v1 (included in URL path)
- Backward compatibility maintained for minor updates
- Major changes will increment version number

## Support and Documentation
- Full API documentation: `API_DOCUMENTATION.md`
- Postman collection: `University_Vendor_App_API.postman_collection.json`
- Quick reference: `API_ENDPOINTS_SUMMARY.md`
- Test script: `test_api.py`

## Common Integration Patterns

### 1. Login and Store Tokens
```javascript
// Example in JavaScript
const loginResponse = await fetch('/api/users/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
});

const { access, refresh, user } = await loginResponse.json();
localStorage.setItem('access_token', access);
localStorage.setItem('refresh_token', refresh);
localStorage.setItem('user', JSON.stringify(user));
```

### 2. Authenticated API Calls
```javascript
const response = await fetch('/api/orders/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
  }
});
```

### 3. Handle Token Expiration
```javascript
if (response.status === 401) {
  // Token expired, refresh it
  const refreshResponse = await fetch('/api/token/refresh/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      refresh: localStorage.getItem('refresh_token') 
    })
  });
  
  const { access } = await refreshResponse.json();
  localStorage.setItem('access_token', access);
  // Retry original request
}
```

This completes the comprehensive API integration package for your frontend developer!
