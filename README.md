# University Vendor App - Backend

A Django REST API backend for a university food ordering and delivery platform. This system enables students to order meals from campus cafeterias and have them delivered by fellow students.

## 🚀 Features

### User Management
- **Three User Types**: Students, Vendors (Cafeterias), and Delivery Personnel
- **JWT Authentication**: Secure token-based authentication
- **User Profiles**: Customizable profiles with campus location and contact info

### Order Management
- **Place Orders**: Students can browse menus and place orders
- **Order Tracking**: Real-time status updates from placement to delivery
- **Status Workflow**: Pending → Confirmed → Preparing → Ready for Delivery → Out for Delivery → Delivered

### Chat System
- **Order-based Chat**: Communication between students, vendors, and delivery personnel
- **Real-time Messaging**: Context-aware messaging for each order
- **Message History**: Complete chat history for each order

### Delivery System
- **Delivery Assignment**: Vendors can assign delivery personnel
- **Availability Management**: Delivery personnel can toggle their availability
- **Campus-based Matching**: Location-based delivery assignment

## 🛠️ Tech Stack

- **Backend**: Django 5.2.3
- **API**: Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Real-time**: Django Channels (WebSocket support)
- **Image Handling**: Pillow

## 📦 Installation

### Prerequisites
- Python 3.10+
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd iRefuel
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## 🔗 API Endpoints

### Authentication
- `POST /api/signup/` - Register new user
- `POST /api/login/` - User login
- `GET /api/profile/` - Get/update user profile

### Cafeterias & Menu (Students)
- `GET /api/cafeterias/` - List all cafeterias
- `GET /api/cafeterias/{id}/` - Get cafeteria details
- `GET /api/cafeterias/{id}/menu/` - Get cafeteria menu

### Orders (Students)
- `POST /api/orders/` - Place new order
- `GET /api/orders/my-orders/` - Get user's orders
- `GET /api/orders/{id}/` - Get order details

### Vendor Management
- `GET /api/orders/vendor/` - Get vendor's orders
- `PATCH /api/orders/{id}/status/` - Update order status
- `GET /api/vendor/cafeteria/` - Get vendor's cafeteria
- `GET /api/vendor/menu-items/` - Manage menu items

### Delivery
- `GET /api/delivery/requests/` - Get delivery assignments
- `GET /api/delivery/requests/available/` - Get available deliveries
- `PATCH /api/delivery/requests/{id}/status/` - Update delivery status
- `PATCH /api/delivery/availability/toggle/` - Toggle availability

### Chat
- `GET /api/chat/orders/{order_id}/` - Get order chat messages
- `POST /api/chat/send/` - Send message
- `GET /api/chat/rooms/` - Get user's chat rooms

## 📊 Database Models

### CustomUser
- Extended Django User with user_type (student/vendor/delivery)
- Campus location and availability tracking

### Cafeteria & MenuItem
- Vendor-owned cafeterias with menu management
- Category-based menu items with pricing

### Order & OrderItem
- Complete order workflow without payments
- Multi-item orders with quantity tracking

### Chat System
- Order-based messaging between all parties
- Read status tracking

### Delivery Management
- Delivery personnel location and availability
- Order assignment and status tracking

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
# For production:
# DATABASE_URL=postgresql://user:password@localhost:5432/irefuel_db
```

### Database Configuration
- **Development**: SQLite (default)
- **Production**: PostgreSQL (configure in settings.py)

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📱 Frontend Integration

This backend is designed to work with Flutter mobile apps:
- **Student App**: Browse, order, track, chat
- **Vendor App**: Manage orders, menu, communicate
- **Delivery App**: Accept deliveries, update status, navigate

### API Response Format
```json
{
  "user": {
    "id": 1,
    "username": "student1",
    "user_type": "student",
    "email": "student@university.edu"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG=False`
2. Configure PostgreSQL database
3. Set up Redis for Django Channels
4. Configure static/media file serving
5. Set up CORS for frontend domains
6. Configure SSL/HTTPS

### Docker Support (Optional)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 📝 Admin Interface

Access the Django admin at `/admin/` to:
- Manage users and permissions
- View and edit orders
- Monitor chat messages
- Configure delivery locations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the existing issues
2. Create a new issue with detailed description
3. Include error logs and reproduction steps

---

Built with ❤️ for university communities
#   i R e f u e l  
 #   i R e f u e l  
 