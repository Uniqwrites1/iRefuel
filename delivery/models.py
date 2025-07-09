from django.db import models
from django.contrib.auth import get_user_model
from orders.models import Order

User = get_user_model()


class DeliveryRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_request')
    delivery_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivery_requests', limit_choices_to={'user_type': 'delivery'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    pickup_time = models.DateTimeField(null=True, blank=True)
    delivered_time = models.DateTimeField(null=True, blank=True)
    delivery_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery Request for Order #{self.order.id} by {self.delivery_person.username}"


class DeliveryPersonLocation(models.Model):
    """Location data for delivery personnel"""
    delivery_person = models.OneToOneField(User, on_delete=models.CASCADE, related_name='location_info', limit_choices_to={'user_type': 'delivery'})
    campus_area = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    current_orders_count = models.PositiveIntegerField(default=0)
    max_orders = models.PositiveIntegerField(default=3)  # Most orders they can handle
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.delivery_person.username} - {self.campus_area} ({'Available' if self.is_available else 'Busy'})"
