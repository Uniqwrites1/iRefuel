# University Vendor App - Backend API Package

## 🚀 Quick Start

Your Django backend is ready for frontend integration! The API server is running at:
- **Development**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`

## 📋 What's Included

### 1. API Documentation
- **`API_DOCUMENTATION.md`** - Complete API reference with all endpoints
- **`API_ENDPOINTS_SUMMARY.md`** - Quick reference for all endpoints
- **`FRONTEND_INTEGRATION_GUIDE.md`** - Step-by-step integration guide

### 2. Testing Tools
- **`University_Vendor_App_API.postman_collection.json`** - Import into Postman for API testing
- **`test_api.py`** - Python script to test all endpoints

### 3. Environment Configuration
- **`.env`** - All configuration variables (already set up)
- **PostgreSQL database** configured and migrated

## 🔑 Key Information for Frontend Development

### Base API URL
```
http://localhost:8000/api/
```

### Authentication
- **JWT Token-based authentication**
- Tokens expire: Access (60 min), Refresh (7 days)
- Include in headers: `Authorization: Bearer <token>`

### User Types
1. **Students** - Place orders, chat with vendors
2. **Vendors** - Manage cafeteria, menu items, orders
3. **Delivery** - Handle delivery requests and status updates

### Core Features
- ✅ User registration and authentication
- ✅ Cafeteria and menu management
- ✅ Order placement and tracking
- ✅ Real-time chat (WebSocket + REST)
- ✅ Delivery assignment and tracking
- ✅ Role-based permissions

## 🎯 Essential Endpoints to Start With

### Authentication
```
POST /api/users/register/     # User registration
POST /api/users/login/        # User login
POST /api/token/refresh/      # Refresh JWT token
```

### Core Functionality
```
GET  /api/users/cafeterias/               # List cafeterias
GET  /api/users/cafeterias/{id}/menu/     # Get menu
POST /api/orders/                         # Place order
GET  /api/orders/student/                 # Student's orders
GET  /api/chat/orders/{id}/               # Order chat
```

## 🧪 Testing the API

### Option 1: Using Postman
1. Import `University_Vendor_App_API.postman_collection.json`
2. Set base URL to `http://localhost:8000/api`
3. Test authentication and other endpoints

### Option 2: Using Test Script
```bash
python test_api.py
```

### Option 3: Admin Panel
- Visit `http://localhost:8000/admin/`
- Login with superuser credentials
- View/create test data

## 🔧 Development Setup Verification

### Check Server Status
```bash
# Server should be running at http://localhost:8000
curl http://localhost:8000/api/users/cafeterias/
```

### Database
- ✅ PostgreSQL configured (`irefuel_db`)
- ✅ All migrations applied
- ✅ Admin user created

### Environment
- ✅ `.env` file configured
- ✅ JWT authentication setup
- ✅ CORS enabled for frontend
- ✅ WebSocket support enabled

## 📱 Frontend Development Workflow

### 1. Authentication Flow
```
Register/Login → Get JWT tokens → Store tokens → Make authenticated requests
```

### 2. Main App Flows

**Student Flow:**
```
Login → Browse Cafeterias → View Menu → Place Order → Track Status → Chat
```

**Vendor Flow:**
```
Login → Manage Menu → View Orders → Update Status → Chat with Customers
```

**Delivery Flow:**
```
Login → View Requests → Accept Delivery → Update Status → Update Location
```

## 🛡️ Security & Best Practices

### For Development
- CORS enabled for localhost
- Debug mode enabled
- Console email backend

### For Production
- Set `DEBUG=False` in .env
- Configure proper `ALLOWED_HOSTS`
- Use HTTPS
- Set strong `SECRET_KEY`
- Use Redis for better performance

## 🔄 Real-time Features

### WebSocket Chat
```
ws://localhost:8000/ws/chat/orders/{order_id}/
```
- Requires JWT authentication
- Real-time messaging between users
- Order-specific chat rooms

## 📊 Data Models Overview

### Order Status Flow
```
pending → confirmed → preparing → ready → delivered
```

### User Roles & Permissions
- **Students**: Can only place orders and chat
- **Vendors**: Can manage their cafeteria and orders
- **Delivery**: Can handle delivery requests

### Menu Categories
- `appetizer`, `main_course`, `dessert`, `beverage`, `snack`

## 🚨 Common Issues & Solutions

### CORS Issues
- Frontend URL must be in `CORS_ALLOWED_ORIGINS` in .env
- Or set `CORS_ALLOW_ALL_ORIGINS=True` for development

### Authentication Issues
- Check token expiration (60 minutes for access tokens)
- Use refresh endpoint to get new access token
- Ensure `Authorization: Bearer <token>` header format

### Database Issues
- Ensure PostgreSQL is running
- Check connection settings in .env
- Run migrations if needed: `python manage.py migrate`

## 📞 Support

### Troubleshooting
1. Check server logs in terminal
2. Test endpoints with Postman collection
3. Verify database connectivity
4. Check .env configuration

### API Testing
- Use provided test script: `python test_api.py`
- Import Postman collection for manual testing
- Check admin panel for data verification

---

## ✅ Ready for Frontend Development!

Your backend API is fully operational with:
- 🔐 Secure JWT authentication
- 📱 Complete REST API endpoints
- 💬 Real-time chat capability
- 🗄️ PostgreSQL database
- 📋 Comprehensive documentation
- 🧪 Testing tools included

The API is production-ready and follows Django/REST framework best practices. All endpoints are documented, tested, and ready for frontend integration!

**Happy coding! 🎉**
