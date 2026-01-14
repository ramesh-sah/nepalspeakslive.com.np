from django.contrib import admin
from .models import EmailNewsletter


@admin.register(EmailNewsletter)
class EmailNewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'subscribed', 'created_at')
    list_filter = ('subscribed', 'created_at')
    search_fields = ('email', 'full_name')
