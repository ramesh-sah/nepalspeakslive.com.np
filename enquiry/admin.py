from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
from io import StringIO
import csv
from .models import Enquiry



@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'formatted_phone', 'country_code', 'created_at', 'status')
    list_filter = ('country_code', 'status', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number', 'inquiry')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('full_name', 'email', 'country_code', 'phone_number', 'status')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    

    def formatted_phone(self, obj):
        """Display phone number with country code in a consistent format."""
        return format_html('<span class="font-mono">+{} {}</span>', obj.country_code, obj.phone_number)
    formatted_phone.short_description = 'Phone Number'

    # Custom CSV Export Action
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        """Export selected enquiries to a downloadable CSV file."""
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(['Full Name', 'Email', 'Phone', 'Country Code', 'Created At', 'Status', 'Inquiry'])

        for enquiry in queryset:
            writer.writerow([
                enquiry.full_name,
                enquiry.email,
                f"+{enquiry.country_code}{enquiry.phone_number}",
                enquiry.country_code,
                enquiry.created_at.strftime("%Y-%m-%d %H:%M"),
                enquiry.status,
                enquiry.inquiry
            ])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=enquiries.csv'
        return response
    export_as_csv.short_description = "Export selected enquiries as CSV"

    class Media:
        css = {
            'all': ('css/admin/enquiry.css',)
        }
