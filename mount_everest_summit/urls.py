from django.views.static import serve


from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from mount_everest_summit.views import AdvertiseWithUs, EmailNewsletterView, HomePage, MountEverestSouth,MountEverestNorth, NewsDetailView,TermsAndConditions,ContactUs,PrivacyPolicy ,RegistrationView ,NewsView

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from accounts.sitemaps import CustomRegistrationSitemap,CustomUserLoginSitemap
from advertising_channel.sitemaps import AdvertisingInquirySitemap,AdPlacementSitemap
from chatbot_app.sitemaps import ChatbotHomeSitemap,ConversationSitemap 
from emailnewsletter.sitemaps import NewsletterHomeSitemap,EmailNewsletterSitemap
from enquiry.sitemaps import ContactUsPageSitemap,EnquirySitemap
from news.sitemaps import NewsCategorySitemap,NewsSubCategorySitemap,NewsSitemap,StaticSitemap
from weather.sitemaps import WeatherStaticSitemap


sitemaps = {
    'login': CustomUserLoginSitemap,
    'register':CustomRegistrationSitemap,
      'advertising_inquiries': AdvertisingInquirySitemap,
    'ad_placements': AdPlacementSitemap,
     'chatbot-home': ChatbotHomeSitemap,
    'chatbot-conversations': ConversationSitemap,
      'newsletter-home': NewsletterHomeSitemap,
    'newsletter-subscribers': EmailNewsletterSitemap,
         "contact-us": ContactUsPageSitemap,
    "enquiries": EnquirySitemap,
     'news': NewsSitemap,
    'categories': NewsCategorySitemap,
    'subcategories': NewsSubCategorySitemap,
    'static': StaticSitemap,
    "weather": WeatherStaticSitemap,
    
}


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # ✅ this line fixes the error
    path('admin/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('',HomePage.as_view(),name='home'),
    path('mount-everest-south/',MountEverestSouth.as_view(),name='mount-everest-south'),
    path('mount-everest-north/',MountEverestNorth.as_view(),name='mount-everest-north'),
    path('news/',NewsView.as_view(),name='news'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),
    path('term-condition/',TermsAndConditions.as_view(),name='term-condition'),
    path('contact-us/',ContactUs.as_view(),name='contact-us'),
    path('newsletter/', EmailNewsletterView.as_view(), name='newsletter'),
    path('advertise-with-us/',AdvertiseWithUs.as_view(),name='advertise-with-us'),
    path('privacy-policy/',PrivacyPolicy.as_view(),name='privacy-policy'),
    
    path('registration/',RegistrationView.as_view(),name='registration'),
    path('weather/', include('weather.urls')),
    path('chat/', include('chatbot_app.urls')),


     path('ckeditor/', include('ckeditor_uploader.urls')),

    #  path('robots.txt', TemplateView.as_view(), name='robots_txt'),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"
        ),
        name="robots"
    ),
    #  path('robots.txt', RobotsTxtView.as_view(), name='robots_txt'),
     path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django-sitemap'),
     

]

if settings.DEBUG:
    # Dev: Django serves static & media automatically
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Production: only for testing, not recommended for real deployment
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]