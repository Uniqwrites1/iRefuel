from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DeliveryRequest, DeliveryPersonLocation

User = get_user_model()


class DeliveryRequestSerializer(serializers.ModelSerializer):
    order_info = serializers.SerializerMethodField()
    delivery_person_name = serializers.CharField(source='delivery_person.get_full_name', read_only=True)

    class Meta:
        model = DeliveryRequest
        fields = ('id', 'order', 'order_info', 'delivery_person', 'delivery_person_name',
                 'status', 'pickup_time', 'delivered_time', 'delivery_notes', 'created_at')
        read_only_fields = ('id', 'delivery_person', 'created_at')

    def get_order_info(self, obj):
        order = obj.order
        return {
            'id': order.id,
            'student_name': order.student.get_full_name(),
            'vendor_name': order.vendor.get_full_name(),
            'total_amount': order.total_amount,
            'delivery_address': order.delivery_address,
            'status': order.status
        }


class DeliveryStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryRequest
        fields = ('status', 'delivery_notes')

    def validate_status(self, value):
        request = self.instance
        current_status = request.status
        
        # Define allowed status transitions
        allowed_transitions = {
            'pending': ['accepted', 'cancelled'],
            'accepted': ['picked_up'],
            'picked_up': ['delivered'],
        }
        
        if current_status not in allowed_transitions:
            raise serializers.ValidationError(f"Cannot transition from {current_status}.")
        
        if value not in allowed_transitions[current_status]:
            raise serializers.ValidationError(
                f"Cannot change status from {current_status} to {value}."
            )
        
        return value


class DeliveryPersonLocationSerializer(serializers.ModelSerializer):
    delivery_person_name = serializers.CharField(source='delivery_person.get_full_name', read_only=True)

    class Meta:
        model = DeliveryPersonLocation
        fields = ('id', 'delivery_person', 'delivery_person_name', 'campus_area',
                 'is_available', 'current_orders_count', 'max_orders', 'last_updated')
        read_only_fields = ('id', 'delivery_person', 'last_updated', 'current_orders_count')


class DeliveryPersonAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPersonLocation
        fields = ('is_available',)
