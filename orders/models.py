from django.db import models
from django.contrib.auth import get_user_model
from users.models import MenuItem

User = get_user_model()


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready_for_delivery', 'Ready for Delivery'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', limit_choices_to={'user_type': 'student'})
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_orders', limit_choices_to={'user_type': 'vendor'})
    delivery_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery_orders', limit_choices_to={'user_type': 'delivery'})
    
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    special_instructions = models.TextField(blank=True, null=True)
    
    estimated_preparation_time = models.PositiveIntegerField(help_text="Estimated time in minutes")
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.student.username} from {self.vendor.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    special_requests = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} for Order #{self.order.id}"


class DeliveryLocation(models.Model):
    """Campus delivery locations"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    coordinates = models.CharField(max_length=100, blank=True, null=True)  # Optional lat,lng
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
