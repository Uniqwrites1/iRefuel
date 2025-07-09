from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    # Delivery requests
    path('requests/', views.DeliveryRequestListView.as_view(), name='delivery-requests'),
    path('requests/available/', views.AvailableDeliveryRequestsView.as_view(), name='available-delivery-requests'),
    path('requests/<int:delivery_id>/status/', views.update_delivery_status, name='update-delivery-status'),
    
    # Delivery personnel management
    path('location/', views.DeliveryPersonLocationView.as_view(), name='delivery-person-location'),
    path('availability/toggle/', views.toggle_availability, name='toggle-availability'),
    
    # For vendors to find nearby delivery personnel
    path('nearby/', views.NearbyDeliveryPersonnelView.as_view(), name='nearby-delivery-personnel'),
    path('assign/<int:order_id>/', views.assign_delivery_person, name='assign-delivery-person'),
    
    # Enhanced delivery management
    path('auto-assign/<int:order_id>/', views.auto_assign_delivery, name='auto-assign-delivery'),
    path('statistics/', views.delivery_statistics, name='delivery-statistics'),
    path('complete/<int:delivery_id>/', views.complete_delivery, name='complete-delivery'),
]
