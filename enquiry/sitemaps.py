from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Enquiry


class ContactUsPageSitemap(Sitemap):
    """
    Static sitemap entry for the Contact Us page.
    Ensures search engines can find and prioritize your contact form page.
    """
    changefreq = "monthly"
    priority = 0.9
    protocol = "https"

    def items(self):
        return ["contact-us"]

    def location(self, item):
        return reverse(item)


class EnquirySitemap(Sitemap):
    """
    Sitemap for Enquiry model entries.
    If enquiries are private (like contact form submissions), 
    we’ll safely map them back to the contact-us page.
    """
    changefreq = "weekly"
    priority = 0.6
    protocol = "https"

    def items(self):
        # Only include resolved or public enquiries (for SEO safety)
        return Enquiry.objects.filter(status="resolved").order_by('id')

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        # Since no detail page exists in the URLconf, 
        # link all entries to the 'contact-us' page.
        return reverse("contact-us")
