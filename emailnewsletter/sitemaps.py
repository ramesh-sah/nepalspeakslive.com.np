from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import EmailNewsletter

class NewsletterHomeSitemap(Sitemap):
    """
    Sitemap entry for the newsletter subscription page.
    Helps search engines discover and index your newsletter form.
    """
    changefreq = "monthly"
    priority = 0.8
    protocol = "https"

    def items(self):
        # Static page for the newsletter form route
        return ["home"]

    def location(self, item):
        return reverse(item)


class EmailNewsletterSitemap(Sitemap):
    """
    Sitemap for all active subscribers (SEO purpose: optional if you show public profiles or archives).
    If this data is private, keep only NewsletterHomeSitemap.
    """
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        # Include only active subscribers if they’re visible (public use-case)
        return EmailNewsletter.objects.filter(subscribed=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # Optional: link to a subscriber details or confirmation page if it exists.
        # If not, you can safely point all to the newsletter root.
        return reverse("home")
