from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Conversation

class ChatbotHomeSitemap(Sitemap):
    """
    Sitemap for the chatbot main page (/chat/).
    Ensures the root chat entry point is indexed for SEO.
    """
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        # Static entry for main chatbot interface
        return ["home"]

    def location(self, item):
        return reverse(item)


class ConversationSitemap(Sitemap):
    """
    Sitemap for individual chatbot conversations.
    Each conversation can be indexed if accessible via a detail view.
    """
    changefreq = "daily"
    priority = 0.7
    protocol = "https"

    def items(self):
        return Conversation.objects.all().order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # Assumes your conversation detail URL is defined as:
        # path('chat/conversation/<int:pk>/', ConversationDetailView.as_view(), name='conversation-detail')
        return reverse('home')
