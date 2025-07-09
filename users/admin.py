from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Cafeteria, MenuItem


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'campus_location', 'profile_picture', 'is_available')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'campus_location')
        }),
    )


@admin.register(Cafeteria)
class CafeteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'vendor__username', 'location')
    raw_id_fields = ('vendor',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'cafeteria', 'price', 'category', 'is_available', 'preparation_time')
    list_filter = ('category', 'is_available', 'cafeteria', 'created_at')
    search_fields = ('name', 'cafeteria__name')
    raw_id_fields = ('cafeteria',)
