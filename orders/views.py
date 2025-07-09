from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Order, OrderItem, DeliveryLocation
from .serializers import (
    OrderCreateSerializer, OrderSerializer, OrderStatusUpdateSerializer,
    DeliveryLocationSerializer
)

User = get_user_model()


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.user_type != 'student':
            raise PermissionDenied("Only students can place orders.")
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Return the created order with full details including ID
        order_serializer = OrderSerializer(order)
        headers = self.get_success_headers(order_serializer.data)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StudentOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type != 'student':
            raise PermissionDenied("Only students can access this.")
        return Order.objects.filter(student=self.request.user)


class VendorOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type != 'vendor':
            raise PermissionDenied("Only vendors can access this.")
        return Order.objects.filter(vendor=self.request.user)


class DeliveryOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type != 'delivery':
            raise PermissionDenied("Only delivery personnel can access this.")
        return Order.objects.filter(delivery_person=self.request.user)


class AvailableDeliveriesView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type != 'delivery':
            raise PermissionDenied("Only delivery personnel can access this.")
        return Order.objects.filter(
            status='ready_for_delivery',
            delivery_person__isnull=True
        )


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'student':
            return Order.objects.filter(student=user)
        elif user.user_type == 'vendor':
            return Order.objects.filter(vendor=user)
        elif user.user_type == 'delivery':
            return Order.objects.filter(delivery_person=user)
        return Order.objects.none()


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Check permissions
    user = request.user
    if user.user_type == 'vendor' and order.vendor != user:
        raise PermissionDenied("You can only update your own orders.")
    elif user.user_type == 'delivery' and order.delivery_person != user:
        raise PermissionDenied("You can only update orders assigned to you.")
    elif user.user_type == 'student':
        raise PermissionDenied("Students cannot update order status.")
    
    serializer = OrderStatusUpdateSerializer(
        order, 
        data=request.data, 
        partial=True,
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    
    # Update timestamps based on status
    new_status = serializer.validated_data['status']
    if new_status == 'confirmed':
        order.confirmed_at = timezone.now()
    elif new_status == 'delivered':
        order.delivered_at = timezone.now()
    
    serializer.save()
    
    return Response({
        'message': f'Order status updated to {new_status}',
        'order': OrderSerializer(order).data
    })


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def accept_delivery(request, order_id):
    if request.user.user_type != 'delivery':
        raise PermissionDenied("Only delivery personnel can accept deliveries.")
    
    order = get_object_or_404(Order, id=order_id, status='ready_for_delivery')
    
    if order.delivery_person is not None:
        return Response(
            {'error': 'This order has already been assigned to a delivery person.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    order.delivery_person = request.user
    order.save()
    
    return Response({
        'message': 'Delivery accepted successfully',
        'order': OrderSerializer(order).data
    })


class DeliveryLocationListView(generics.ListAPIView):
    queryset = DeliveryLocation.objects.filter(is_active=True)
    serializer_class = DeliveryLocationSerializer
    permission_classes = [permissions.IsAuthenticated]
