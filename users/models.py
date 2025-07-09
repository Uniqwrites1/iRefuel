from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('vendor', 'Vendor'),
        ('delivery', 'Delivery Personnel'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    campus_location = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_available = models.BooleanField(default=True)  # For delivery personnel availability
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Cafeteria(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    vendor = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'vendor'})
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    cafeteria = models.ForeignKey(Cafeteria, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50)  # such as 'main_course', 'dessert', 'beverage'
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    preparation_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.cafeteria.name}"
