from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user_name', 'user_email', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'user_name', 'user_email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Conversation Info', {
            'fields': ('title', 'created_at', 'updated_at')
        }),
        ('User Information', {
            'fields': ('user_name', 'user_email', 'user_phone', 'user_address', 'user_country', 'user_notes'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'role', 'content_preview', 'triggered_info_collection', 'timestamp']
    list_filter = ['role', 'timestamp', 'triggered_info_collection']
    search_fields = ['content', 'conversation__title']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'