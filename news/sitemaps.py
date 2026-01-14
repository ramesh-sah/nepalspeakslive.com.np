from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import News, NewsCategory, NewsSubCategory


# ------------------------------
# 📰 News Sitemap
# ------------------------------
class NewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        # Include only published news for SEO visibility
        return News.objects.filter(is_published=True).order_by('-published_date')

    def lastmod(self, obj):
        return obj.published_date
    
    

     # Add images to sitemap
    def images(self, obj):
        # Collect all images associated with the news
        return [
            {'location': img.image.url, 'title': img.caption or obj.title}
            for img in obj.images.all()
        ]

    # Add videos to sitemap
    def videos(self, obj):
        return [
            {'thumbnail_loc': vid.video.url, 'title': vid.caption or obj.title, 'content_loc': vid.video.url}
            for vid in obj.videos.all()
        ]

    def location(self, obj):
        # Matches your URL pattern: path('news/<slug:slug>/', ...)
        return reverse('news-detail', args=[obj.slug])


# ------------------------------
# 🗂️ News Category Sitemap
# ------------------------------
class NewsCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return NewsCategory.objects.all().order_by('name')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # You don’t currently have a category detail URL — 
        # uncomment below if you plan to add one like:
        # path('news/category/<slug:slug>/', ...)
        # return reverse('news-category', args=[obj.slug])
        return reverse('news')  # fallback → sends bots to the main news listing


# ------------------------------
# 🏷️ News SubCategory Sitemap
# ------------------------------
class NewsSubCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return NewsSubCategory.objects.all().order_by('name')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # Same note as above — adjust if you later add subcategory URLs
        return reverse('news')


# ------------------------------
# 🏔️ Static / Mount Everest Pages Sitemap
# ------------------------------
class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return [
            'home',
            'mount-everest-south',
            'mount-everest-north',
            'news',
            'term-condition',
            'contact-us',
            'newsletter',
            'advertise-with-us',
            'privacy-policy',
            'registration',
        ]

    def location(self, item):
        return reverse(item)



