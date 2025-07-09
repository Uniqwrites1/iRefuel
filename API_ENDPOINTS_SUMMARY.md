# API Endpoints Quick Reference

## Authentication
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - User login
- `POST /api/token/refresh/` - Refresh JWT token

## User Management
- `GET /api/users/profile/` - Get user profile
- `PATCH /api/users/profile/` - Update user profile

## Cafeterias & Menus (Students)
- `GET /api/users/cafeterias/` - List all cafeterias
- `GET /api/users/cafeterias/{id}/menu/` - Get cafeteria menu

## Vendor Management
- `GET /api/users/vendor/cafeteria/` - Get vendor's cafeteria
- `GET /api/users/vendor/menu-items/` - List vendor's menu items
- `POST /api/users/vendor/menu-items/` - Create menu item
- `GET /api/users/vendor/menu-items/{id}/` - Get specific menu item
- `PATCH /api/users/vendor/menu-items/{id}/` - Update menu item
- `DELETE /api/users/vendor/menu-items/{id}/` - Delete menu item

## Orders
- `POST /api/orders/` - Place order (Students)
- `GET /api/orders/student/` - Get student's orders
- `GET /api/orders/vendor/` - Get vendor's orders
- `GET /api/orders/delivery/` - Get delivery orders
- `PATCH /api/orders/{id}/status/` - Update order status (Vendors)
- `GET /api/orders/delivery-locations/` - List delivery locations

## Chat
- `POST /api/chat/send/` - Send message
- `GET /api/chat/orders/{order_id}/` - Get order chat messages
- `POST /api/chat/orders/{order_id}/mark-read/` - Mark messages as read

## Delivery
- `GET /api/delivery/requests/` - Get delivery requests
- `POST /api/delivery/requests/{id}/accept/` - Accept delivery request
- `PATCH /api/delivery/requests/{id}/status/` - Update delivery status
- `POST /api/delivery/toggle-availability/` - Toggle availability
- `POST /api/delivery/update-location/` - Update delivery location

## WebSocket
- `ws://localhost:8000/ws/chat/orders/{order_id}/` - Real-time chat

## Base URL
- Development: `http://localhost:8000/api/`
- Production: `https://your-domain.com/api/`

## Authentication Header
```
Authorization: Bearer <access_token>
```

## User Types
- `student` - Can place orders, chat
- `vendor` - Can manage cafeteria, menu, orders
- `delivery` - Can handle deliveries

## Order Status Flow
`pending` → `confirmed` → `preparing` → `ready` → `delivered`

## Delivery Status Flow
`assigned` → `picked_up` → `delivered`
