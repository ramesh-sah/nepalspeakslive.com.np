from .models import NewsCategory

def news_categories(request):
    """
    This context processor makes the list of all news categories available in every template.
    """
    categories = NewsCategory.objects.all()
    return {'news_categories': categories}
