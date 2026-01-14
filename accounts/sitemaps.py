# account/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import CustomUser

class CustomUserLoginSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        # Return only users that you want publicly accessible
        return CustomUser.objects.filter(is_active=True).order_by('id')

    def lastmod(self, obj):
        return obj.last_updated
    

    def location(self, obj):
        # Return URL for the user profile page
        return f"/admin/"  # adjust URL to your profile view

    

class CustomRegistrationSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        # Return only users that you want publicly accessible
        return CustomUser.objects.filter(is_active=True).order_by('id')

    def lastmod(self, obj):
        return obj.last_updated
    

    def location(self, obj):
        # Return URL for the user profile page
        return f"/registration/"  # adjust URL to your profile view

    

