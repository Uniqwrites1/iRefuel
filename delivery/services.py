"""
Services for delivery management
"""
import math
from typing import List, Optional
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from .models import DeliveryRequest, DeliveryPersonLocation
from orders.models import Order

User = get_user_model()


class DeliveryAssignmentService:
    """Service for delivery assignment"""
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        Returns distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    @classmethod
    def find_available_delivery_personnel(cls, order: Order, max_distance: float = 2.0) -> List[User]:
        """
        Find available delivery personnel near the order location
        """
        available_personnel = User.objects.filter(
            user_type='delivery',
            is_available=True,
            is_active=True
        ).select_related('location_info')
        
        suitable_personnel = []
        
        for person in available_personnel:
            # Check if they have location info
            if not hasattr(person, 'location_info'):
                continue
                
            location_info = person.location_info
            
            # Check if they're available and not at max capacity
            if (location_info.is_available and 
                location_info.current_orders_count < location_info.max_orders):
                
                # Campus area matching with coordinates support
                if cls._is_in_service_area(person, order):
                    suitable_personnel.append(person)
        
        return suitable_personnel
    
    @staticmethod
    def _is_in_service_area(delivery_person: User, order: Order) -> bool:
        """
        Check if delivery person serves the order's area
        This is a simplified version - can be enhanced with actual coordinates
        """
        delivery_area = delivery_person.location_info.campus_area.lower()
        order_area = order.delivery_address.lower()
        
        # Keyword matching for campus areas
        campus_areas = {
            'north': ['north', 'library', 'science', 'engineering'],
            'south': ['south', 'sports', 'gym', 'stadium'],
            'east': ['east', 'dormitory', 'hostel', 'residence'],
            'west': ['west', 'cafeteria', 'dining', 'food'],
            'central': ['central', 'admin', 'main', 'center']
        }
        
        for area, keywords in campus_areas.items():
            if area in delivery_area:
                return any(keyword in order_area for keyword in keywords)
        
        return True  # Default to available if no specific area matching
    
    @classmethod
    @transaction.atomic
    def assign_delivery_person(cls, order: Order, delivery_person: User = None) -> Optional[DeliveryRequest]:
        """
        Assign a delivery person to an order
        """
        if delivery_person is None:
            # Assign based on availability and location
            available_personnel = cls.find_available_delivery_personnel(order)
            if not available_personnel:
                return None
            
            # Select the person with the lowest current orders count
            delivery_person = min(
                available_personnel,
                key=lambda p: p.location_info.current_orders_count
            )
        
        # Create delivery assignment
        delivery_request = DeliveryRequest.objects.create(
            order=order,
            delivery_person=delivery_person,
            status='pending'
        )
        
        # Update order status and assign delivery person
        order.delivery_person = delivery_person
        order.status = 'ready_for_delivery'
        order.save()
        
        # Update delivery person's current orders count
        location_info = delivery_person.location_info
        location_info.current_orders_count += 1
        location_info.save()
        
        return delivery_request
    
    @classmethod
    @transaction.atomic
    def complete_delivery(cls, delivery_request: DeliveryRequest) -> bool:
        """
        Mark delivery as completed and update counters
        """
        delivery_request.status = 'delivered'
        delivery_request.delivered_time = timezone.now()
        delivery_request.save()
        
        # Update order status
        order = delivery_request.order
        order.status = 'delivered'
        order.delivered_at = timezone.now()
        order.save()
        
        # Decrease delivery person's current orders count
        location_info = delivery_request.delivery_person.location_info
        location_info.current_orders_count = max(0, location_info.current_orders_count - 1)
        location_info.save()
        
        return True
    
    @classmethod
    def get_delivery_statistics(cls, delivery_person: User) -> dict:
        """
        Get delivery statistics for a delivery person
        """
        delivered_orders = DeliveryRequest.objects.filter(
            delivery_person=delivery_person,
            status='delivered'
        ).count()
        
        pending_orders = DeliveryRequest.objects.filter(
            delivery_person=delivery_person,
            status__in=['pending', 'accepted', 'picked_up']
        ).count()
        
        return {
            'total_delivered': delivered_orders,
            'current_orders': pending_orders,
            'is_available': delivery_person.location_info.is_available if hasattr(delivery_person, 'location_info') else False
        }


class NotificationService:
    """Service for sending real-time notifications"""
    
    @staticmethod
    def notify_order_update(order: Order, message: str):
        """Send order update notification"""
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        
        # Tell all involved users
        users_to_notify = [order.student, order.vendor]
        if order.delivery_person:
            users_to_notify.append(order.delivery_person)
        
        for user in users_to_notify:
            async_to_sync(channel_layer.group_send)(
                f'user_{user.id}',
                {
                    'type': 'order_update',
                    'order_id': order.id,
                    'status': order.status,
                    'message': message
                }
            )
    
    @staticmethod
    def notify_new_message(chat_message):
        """Send new message notification"""
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        
        # Tell the receiver
        async_to_sync(channel_layer.group_send)(
            f'user_{chat_message.receiver.id}',
            {
                'type': 'new_message',
                'order_id': chat_message.order.id,
                'sender_name': chat_message.sender.get_full_name(),
                'message': chat_message.message[:50] + '...' if len(chat_message.message) > 50 else chat_message.message
            }
        )
    
    @staticmethod
    def notify_delivery_assignment(order: Order):
        """Send delivery assignment notification"""
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        
        if order.delivery_person:
            async_to_sync(channel_layer.group_send)(
                f'user_{order.delivery_person.id}',
                {
                    'type': 'delivery_request',
                    'order_id': order.id,
                    'location': order.delivery_address,
                    'amount': str(order.total_amount)
                }
            )
