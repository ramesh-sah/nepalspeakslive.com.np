# admin.py
from django.contrib import admin
from . models import AdvertisingInquiry, AdPlacement



@admin.register(AdvertisingInquiry)
class AdvertisingInquiryAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'contact_person',
        'email',
        'budget',
        'submitted_at',
        'terms_accepted',
        'status',
    )
    list_filter = ('budget', 'submitted_at', 'terms_accepted', 'status')
    search_fields = ('company_name', 'contact_person', 'email', 'website')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)

    fieldsets = (
        (None, {
            'fields': (
                'company_name', 
                'contact_person', 
                'email', 
                'phone', 
                'website',
                'budget', 
                'channels', 
                'message', 
                'marketing_materials', 
                'terms_accepted', 
                'submitted_at',
                'status',
            )
        }),
    )


@admin.register(AdPlacement)
class AdPlacementAdmin(admin.ModelAdmin):
    list_display = (
        'inquiry',
        'placement',
        'start_date',
        'end_date',
        'ads_created_by',
    )
    list_filter = ('placement', 'start_date', 'end_date')
    search_fields = ('inquiry__company_name', 'ads_created_by__email')
    ordering = ('-start_date',)

    fieldsets = (
        (None, {
            'fields': (
                'inquiry',
                'placement',
                'start_date',
                'end_date',
                'ads_created_by',
            )
        }),
    )
