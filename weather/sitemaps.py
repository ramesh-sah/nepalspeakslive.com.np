from django.contrib.sitemaps import Sitemap
from django.urls import reverse


# ------------------------------
# 🌤️ Weather App Sitemap
# ------------------------------
class WeatherStaticSitemap(Sitemap):
    changefreq = "hourly"  # Weather updates often — good for SEO freshness
    priority = 0.9

    def items(self):
        return [
            "everest_weather_clean",  # Main weather page
            "weather_api",            # API endpoint (optional for indexing)
        ]

    def location(self, item):
        return reverse(item)


