from django.contrib import admin
from .models import Order, OrderItem, DeliveryLocation


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'vendor', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at', 'vendor')
    search_fields = ('student__username', 'vendor__username', 'id')
    raw_id_fields = ('student', 'vendor', 'delivery_person')
    readonly_fields = ('total_amount', 'created_at', 'updated_at')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('order__created_at',)
    search_fields = ('order__id', 'menu_item__name')
    raw_id_fields = ('order', 'menu_item')
    readonly_fields = ('subtotal',)


@admin.register(DeliveryLocation)
class DeliveryLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
