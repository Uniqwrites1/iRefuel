from django.contrib import admin
from .models import DeliveryRequest, DeliveryPersonLocation


@admin.register(DeliveryRequest)
class DeliveryRequestAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_person', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__id', 'delivery_person__username')
    raw_id_fields = ('order', 'delivery_person')
    readonly_fields = ('created_at', 'pickup_time', 'delivered_time')


@admin.register(DeliveryPersonLocation)
class DeliveryPersonLocationAdmin(admin.ModelAdmin):
    list_display = ('delivery_person', 'campus_area', 'is_available', 'current_orders_count', 'max_orders')
    list_filter = ('is_available', 'campus_area')
    search_fields = ('delivery_person__username', 'campus_area')
    raw_id_fields = ('delivery_person',)
    readonly_fields = ('last_updated',)
