from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # Cafeterias (Student access)
    path('cafeterias/', views.CafeteriaListView.as_view(), name='cafeteria-list'),
    path('cafeterias/<int:pk>/', views.CafeteriaDetailView.as_view(), name='cafeteria-detail'),
    path('cafeterias/<int:cafeteria_id>/menu/', views.CafeteriaMenuView.as_view(), name='cafeteria-menu'),
    
    # Vendor-specific endpoints
    path('vendor/cafeteria/', views.VendorCafeteriaView.as_view(), name='vendor-cafeteria'),
    path('vendor/menu-items/', views.VendorMenuItemsView.as_view(), name='vendor-menu-items'),
    path('vendor/menu-items/<int:pk>/', views.VendorMenuItemDetailView.as_view(), name='vendor-menu-item-detail'),
]
