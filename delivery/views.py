from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from .models import DeliveryRequest, DeliveryPersonLocation
from .serializers import (
    DeliveryRequestSerializer, DeliveryStatusUpdateSerializer,
    DeliveryPersonLocationSerializer, DeliveryPersonAvailabilitySerializer
)
from .services import DeliveryAssignmentService, NotificationService
from orders.models import Order

User = get_user_model()


class DeliveryRequestListView(generics.ListAPIView):
    serializer_class = DeliveryRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type != 'delivery':
            raise PermissionDenied("Only delivery personnel can access this.")
        return DeliveryRequest.objects.filter(delivery_person=self.request.user)


class AvailableDeliveryRequestsView(generics.ListAPIView):
    serializer_class = DeliveryRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type != 'delivery':
            raise PermissionDenied("Only delivery personnel can access this.")
        return DeliveryRequest.objects.filter(
            status='pending',
            delivery_person__isnull=True
        )


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_delivery_status(request, delivery_id):
    if request.user.user_type != 'delivery':
        raise PermissionDenied("Only delivery personnel can update delivery status.")
    
    delivery_request = get_object_or_404(DeliveryRequest, id=delivery_id)
    
    if delivery_request.delivery_person != request.user:
        raise PermissionDenied("You can only update your own deliveries.")
    
    serializer = DeliveryStatusUpdateSerializer(
        delivery_request,
        data=request.data,
        partial=True
    )
    serializer.is_valid(raise_exception=True)
    
    # Update timestamps based on status
    new_status = serializer.validated_data.get('status')
    if new_status == 'picked_up':
        delivery_request.pickup_time = timezone.now()
    elif new_status == 'delivered':
        delivery_request.delivered_time = timezone.now()
        # Also update the main order status
        delivery_request.order.status = 'delivered'
        delivery_request.order.delivered_at = timezone.now()
        delivery_request.order.save()
    
    serializer.save()
    
    return Response({
        'message': f'Delivery status updated to {new_status}',
        'delivery': DeliveryRequestSerializer(delivery_request).data
    })


class DeliveryPersonLocationView(generics.RetrieveUpdateAPIView):
    serializer_class = DeliveryPersonLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.request.user.user_type != 'delivery':
            raise PermissionDenied("Only delivery personnel can access this.")
        
        location_info, created = DeliveryPersonLocation.objects.get_or_create(
            delivery_person=self.request.user,
            defaults={'campus_area': 'Main Campus', 'is_available': True}
        )
        return location_info


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def toggle_availability(request):
    if request.user.user_type != 'delivery':
        raise PermissionDenied("Only delivery personnel can update availability.")
    
    location_info, created = DeliveryPersonLocation.objects.get_or_create(
        delivery_person=request.user,
        defaults={'campus_area': 'Main Campus', 'is_available': True}
    )
    
    # Toggle the availability
    location_info.is_available = not location_info.is_available
    location_info.save()
    
    return Response({
        'message': f'Availability updated to {"available" if location_info.is_available else "unavailable"}',
        'location_info': DeliveryPersonLocationSerializer(location_info).data
    })


class NearbyDeliveryPersonnelView(generics.ListAPIView):
    serializer_class = DeliveryPersonLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type not in ['vendor', 'student']:
            raise PermissionDenied("Only vendors and students can access this.")
        
        return DeliveryPersonLocation.objects.filter(
            is_available=True,
            current_orders_count__lt=models.F('max_orders')
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def assign_delivery_person(request, order_id):
    if request.user.user_type != 'vendor':
        raise PermissionDenied("Only vendors can assign delivery personnel.")
    
    order = get_object_or_404(Order, id=order_id, vendor=request.user)
    
    if order.status != 'ready_for_delivery':
        return Response(
            {'error': 'Order must be ready for delivery to assign delivery person.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    delivery_person_id = request.data.get('delivery_person_id')
    if not delivery_person_id:
        return Response(
            {'error': 'delivery_person_id is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    delivery_person = get_object_or_404(User, id=delivery_person_id, user_type='delivery')
    
    # Check if delivery person is available
    location_info = get_object_or_404(DeliveryPersonLocation, delivery_person=delivery_person)
    if not location_info.is_available or location_info.current_orders_count >= location_info.max_orders:
        return Response(
            {'error': 'Delivery person is not available.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create delivery assignment
    delivery_request = DeliveryRequest.objects.create(
        order=order,
        delivery_person=delivery_person,
        status='pending'
    )
    
    # Update order
    order.delivery_person = delivery_person
    order.save()
    
    # Update delivery person's current orders count
    location_info.current_orders_count += 1
    location_info.save()
    
    return Response({
        'message': 'Delivery person assigned successfully',
        'delivery_request': DeliveryRequestSerializer(delivery_request).data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def auto_assign_delivery(request, order_id):
    """
    Auto assign delivery person by location and availability
    """
    if request.user.user_type != 'vendor':
        return Response(
            {'error': 'Only vendors can assign delivery personnel'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    order = get_object_or_404(Order, id=order_id, vendor=request.user)
    
    if order.status != 'ready_for_delivery':
        return Response(
            {'error': 'Order must be ready for delivery to assign delivery person'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    delivery_request = DeliveryAssignmentService.assign_delivery_person(order)
    
    if delivery_request:
        NotificationService.notify_delivery_assignment(order)
        return Response({
            'message': 'Delivery person assigned successfully',
            'delivery_request': DeliveryRequestSerializer(delivery_request).data
        })
    else:
        return Response(
            {'error': 'No available delivery personnel found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def delivery_statistics(request):
    """
    Get statistics for delivery personnel
    """
    if request.user.user_type != 'delivery':
        return Response(
            {'error': 'Only delivery personnel can access statistics'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    stats = DeliveryAssignmentService.get_delivery_statistics(request.user)
    return Response(stats)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def complete_delivery(request, delivery_id):
    """
    Mark delivery as completed
    """
    if request.user.user_type != 'delivery':
        return Response(
            {'error': 'Only delivery personnel can complete deliveries'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    delivery_request = get_object_or_404(
        DeliveryRequest, 
        id=delivery_id, 
        delivery_person=request.user
    )
    
    if delivery_request.status != 'picked_up':
        return Response(
            {'error': 'Delivery must be picked up before completion'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    success = DeliveryAssignmentService.complete_delivery(delivery_request)
    
    if success:
        NotificationService.notify_order_update(
            delivery_request.order, 
            'Your order has been delivered!'
        )
        return Response({'message': 'Delivery completed successfully'})
    else:
        return Response(
            {'error': 'Failed to complete delivery'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
