from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Chat messages
    path('orders/<int:order_id>/', views.OrderChatMessagesView.as_view(), name='order-chat-messages'),
    path('send/', views.SendMessageView.as_view(), name='send-message'),
    
    # Chat rooms
    path('rooms/', views.UserChatRoomsView.as_view(), name='user-chat-rooms'),
    
    # Utilities
    path('unread-count/', views.UnreadMessagesCountView.as_view(), name='unread-messages-count'),
    path('orders/<int:order_id>/participants/', views.get_order_participants, name='order-participants'),
]
