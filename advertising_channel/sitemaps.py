# advertising_channel/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import AdvertisingInquiry, AdPlacement

class AdvertisingInquirySitemap(Sitemap):
    """
    Sitemap for AdvertisingInquiry pages (only publicly visible inquiries).
    """
    changefreq = "daily"
    priority = 0.8

    def items(self):
        # Include only inquiries where terms are accepted
        return AdvertisingInquiry.objects.filter(terms_accepted=True).order_by('id')

    def lastmod(self, obj):
        return obj.submitted_at

    def location(self, obj):
        # Point to the public page; adjust view name if needed
        return reverse('advertise-with-us')


class AdPlacementSitemap(Sitemap):
    """
    Sitemap for AdPlacement pages.
    """
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return AdPlacement.objects.all().order_by('id')

    def lastmod(self, obj):
        # Could use end_date or start_date depending on recrawl strategy
        return obj.end_date

    def location(self, obj):
        # Point to the public advertise-with-us page
        return reverse('advertise-with-us')
