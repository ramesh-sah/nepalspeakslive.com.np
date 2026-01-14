from django.db import models
from django.utils import timezone
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.conf import settings  # ✅ Correct way to reference AUTH_USER_MODEL
from meta.models import ModelMeta
# -------------------------
# News Category Model
# -------------------------
class NewsCategory(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='news_categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "News Categories"

    def __str__(self):
        return self.name

# -------------------------
# News SubCategory Model
# -------------------------
class NewsSubCategory(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='news_subcategories', on_delete=models.CASCADE)
    category = models.ForeignKey(NewsCategory, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "News SubCategory"
        verbose_name_plural = "News SubCategories"
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category.name} - {self.name}"

# -------------------------
# News Image Model
# -------------------------
class NewsImage(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='news_images', on_delete=models.CASCADE)
    news = models.ForeignKey('News', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news/images/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.news.title}"

# -------------------------
# News Video Model
# -------------------------
class NewsVideo(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='news_videos', on_delete=models.CASCADE)
    news = models.ForeignKey('News', related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='news/videos/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Access the title through the related News object
        return f"Video for {self.news.title}"

# -------------------------
# Main News Model
# -------------------------
class News(models.Model,ModelMeta):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='news', on_delete=models.CASCADE)
    category = models.ForeignKey(NewsCategory, related_name='news', on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(NewsSubCategory, related_name='news', on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False)
    summary = models.TextField(blank=True, null=True, help_text="A short summary of the news article")
    content = RichTextField()
    author = models.CharField(max_length=100, blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)

    featured_image = models.ImageField(upload_to='news/featured/', null=True, blank=True)

    is_trending = models.BooleanField(default=False, help_text="Flag if the article is trending")
    is_breaking = models.BooleanField(default=False, help_text="Flag if the article is breaking news")
    is_latest = models.BooleanField(default=False, help_text="Flag if the article is among the latest")
    is_exclusive = models.BooleanField(default=False, help_text="Flag if the article is exclusive content")
    is_mount_everest_south = models.BooleanField(default=False, help_text="Flag if the article is exclusive content")
    is_mount_everest_north = models.BooleanField(default=False, help_text="Flag if the article is exclusive content")
    

    location = models.CharField(max_length=100, blank=True, null=True, help_text="Location of the event")
    peak_altitude = models.IntegerField(blank=True, null=True, help_text="Peak altitude in meters")
    weather_update = models.CharField(max_length=255, blank=True, null=True, help_text="Latest weather conditions")
    expedition_info = models.TextField(blank=True, null=True, help_text="Details about the expedition or climbing team")
    risk_level = models.CharField(max_length=50, blank=True, null=True, help_text="Risk level (e.g., Low, Moderate, High)")

    tags = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated tags for search and filtering")
    view_count = models.PositiveIntegerField(default=0, help_text="Number of views")
    likes = models.PositiveIntegerField(default=0, help_text="Number of likes")
    shares = models.PositiveIntegerField(default=0, help_text="Number of shares")
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
        
        
   