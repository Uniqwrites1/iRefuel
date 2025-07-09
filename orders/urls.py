from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Order management
    path('', views.OrderCreateView.as_view(), name='order-create'),
    path('my-orders/', views.StudentOrdersView.as_view(), name='student-orders'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:order_id>/status/', views.update_order_status, name='update-order-status'),
    
    # Vendor endpoints
    path('vendor/', views.VendorOrdersView.as_view(), name='vendor-orders'),
    
    # Delivery endpoints
    path('delivery/', views.DeliveryOrdersView.as_view(), name='delivery-orders'),
    path('deliveries/available/', views.AvailableDeliveriesView.as_view(), name='available-deliveries'),
    path('<int:order_id>/accept-delivery/', views.accept_delivery, name='accept-delivery'),
    
    # Delivery locations
    path('delivery-locations/', views.DeliveryLocationListView.as_view(), name='delivery-locations'),
]
