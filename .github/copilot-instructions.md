<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# University Vendor App - Backend Instructions

## Project Overview
This is a Django REST API backend for a university food ordering and delivery platform. The system connects students, vendors (cafeterias), and delivery personnel.

## Architecture Guidelines

### Models
- Use the custom User model (CustomUser) for all user-related operations
- Follow the established model relationships between Order, OrderItem, ChatMessage, etc.
- Maintain proper foreign key relationships and constraints

### API Design
- Follow RESTful conventions
- Use Django REST Framework serializers for data validation
- Implement proper permission classes for different user types
- Return consistent JSON responses with appropriate HTTP status codes

### Authentication
- Use JWT tokens for authentication (djangorestframework-simplejwt)
- Implement role-based access control (student, vendor, delivery)
- Validate user permissions before allowing access to endpoints

### Business Logic
- Students can only place orders, not modify them directly
- Vendors can manage their cafeteria, menu items, and order status
- Delivery personnel can update delivery status and toggle availability
- No payment processing - orders are placed directly without payment gateway

### Error Handling
- Use appropriate HTTP status codes
- Return meaningful error messages
- Handle edge cases (e.g., unavailable menu items, delivery assignment conflicts)

### Database
- Use transactions for complex operations (e.g., order creation with multiple items)
- Implement proper cascading deletes and null handling
- Use select_related/prefetch_related for query optimization

## Code Style
- Follow Django/Python best practices
- Use descriptive variable and function names
- Add docstrings for complex functions
- Keep views focused and delegate business logic to models/serializers

## Testing
- Write unit tests for models, serializers, and views
- Test different user roles and permissions
- Test edge cases and error conditions
- Use Django's TestCase for database-backed tests

## Common Patterns
- Use get_object_or_404 for object retrieval
- Implement proper pagination for list views
- Use serializer validation for complex business rules
- Return user-friendly error messages
