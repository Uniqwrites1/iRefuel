from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Order, OrderItem, DeliveryLocation
from users.models import MenuItem

User = get_user_model()


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_price = serializers.DecimalField(source='menu_item.price', max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'menu_item', 'menu_item_name', 'menu_item_price', 
                 'quantity', 'unit_price', 'subtotal', 'special_requests')
        read_only_fields = ('id', 'unit_price', 'subtotal')

    def create(self, validated_data):
        # Set unit_price from menu_item if not provided
        if 'unit_price' not in validated_data:
            validated_data['unit_price'] = validated_data['menu_item'].price
        return super().create(validated_data)


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('vendor', 'delivery_address', 'special_instructions', 'items')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Calculate total amount and preparation time
        total_amount = 0
        max_prep_time = 0
        
        for item_data in items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            unit_price = menu_item.price
            subtotal = unit_price * quantity
            total_amount += subtotal
            
            # Track longest preparation time
            if menu_item.preparation_time > max_prep_time:
                max_prep_time = menu_item.preparation_time
        
        order = Order.objects.create(
            student=self.context['request'].user,
            total_amount=total_amount,
            estimated_preparation_time=max_prep_time,
            **validated_data
        )
        
        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                unit_price=item_data['menu_item'].price,
                **item_data
            )
        
        return order


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    vendor_name = serializers.CharField(source='vendor.get_full_name', read_only=True)
    delivery_person_name = serializers.CharField(source='delivery_person.get_full_name', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'student', 'student_name', 'vendor', 'vendor_name', 
                 'delivery_person', 'delivery_person_name', 'status', 'total_amount',
                 'delivery_address', 'special_instructions', 'estimated_preparation_time',
                 'estimated_delivery_time', 'created_at', 'updated_at', 
                 'confirmed_at', 'delivered_at', 'items')
        read_only_fields = ('id', 'student', 'total_amount', 'estimated_preparation_time',
                          'created_at', 'updated_at', 'confirmed_at', 'delivered_at')


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)

    def validate_status(self, value):
        order = self.instance
        user = self.context['request'].user
        
        # Define allowed status transitions based on user role
        allowed_transitions = {
            'vendor': {
                'pending': ['confirmed', 'cancelled'],
                'confirmed': ['preparing'],
                'preparing': ['ready_for_delivery'],
            },
            'delivery': {
                'ready_for_delivery': ['out_for_delivery'],
                'out_for_delivery': ['delivered'],
            }
        }
        
        if user.user_type not in allowed_transitions:
            raise serializers.ValidationError("You don't have permission to update order status.")
        
        current_status = order.status
        user_allowed = allowed_transitions[user.user_type]
        
        if current_status not in user_allowed or value not in user_allowed[current_status]:
            raise serializers.ValidationError(f"Cannot change status from {current_status} to {value}.")
        
        return value


class DeliveryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLocation
        fields = ('id', 'name', 'description', 'coordinates', 'is_active')
        read_only_fields = ('id',)
