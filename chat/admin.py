from django.contrib import admin
from .models import ChatMessage, ChatRoom


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'order', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'order__id', 'message')
    raw_id_fields = ('sender', 'receiver', 'order')
    readonly_fields = ('timestamp',)


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('order__id',)
    raw_id_fields = ('order',)
    filter_horizontal = ('participants',)
    readonly_fields = ('created_at',)
