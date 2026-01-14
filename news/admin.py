from django.contrib import admin
from .models import NewsCategory, NewsSubCategory, News, NewsImage, NewsVideo


# -------------------------
# News Category Admin
# -------------------------
@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

# -------------------------
# News SubCategory Admin
# -------------------------
@admin.register(NewsSubCategory)
class NewsSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_by', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'created_at')

# -------------------------
# News Admin
# -------------------------
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'subcategory', 'is_published', 'published_date', 'created_by')
    search_fields = ('title', 'summary', 'content', 'tags')
    list_filter = ('category', 'subcategory', 'is_published', 'is_trending', 'is_breaking', 'is_latest', 'is_exclusive')
    list_editable = ('is_published',)
    ordering = ('-published_date',)

# -------------------------
# News Image Admin
# -------------------------
@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ('news', 'image', 'caption', 'order', 'created_by', 'created_at')
    list_filter = ('news', 'created_at')
    search_fields = ('news__title', 'caption')

# -------------------------
# News Video Admin
# -------------------------
@admin.register(NewsVideo)
class NewsVideoAdmin(admin.ModelAdmin):
    list_display = ('news', 'video', 'caption', 'created_by', 'created_at')
    list_filter = ('news', 'created_at')
    search_fields = ('news__title', 'caption')
