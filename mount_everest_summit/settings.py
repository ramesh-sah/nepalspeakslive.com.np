
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cczl^ckzujb+wj)-25dlz@tql!q0amkb)fgiyv%set3ievm%t-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = [ "http://www.nepalspeakslive.com.np",
    "https://www.nepalspeakslive.com.np",
    "http://nepalspeakslive.com.np",
    "https://nepalspeakslive.com.np",
    "*"
    ]



# Application definition

INSTALLED_APPS = [
          'jazzmin', 
        'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    
    
    #installed app
    'accounts',
    'news',
    'enquiry',
    'advertising_channel', 
    'emailnewsletter',
    'weather',
    'chatbot_app',


    

    
    
    #third party app
    'ckeditor',
   
    
   

 
 
    

  
    
]

MIDDLEWARE = [
   
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'mount_everest_summit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'news.context_processors.news_categories',
                
              
            ],
        },
    },
]

WSGI_APPLICATION = 'mount_everest_summit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'check_same_thread': False,
    }
    
}
# import dj_database_url
# import os

# # Use this for local development (hardcoded URL)
# DATABASE_URL = "mysql://mysql:DS08bZqbL1QSj21BX1ud31w2Q5YklHd8Mx7WQ0Nfb9LAwAhTbcR1XORl5rFLgaxj@fgsck4wo44g8g0skkgw0ksgg:3306/default"

# For production/Coolify: Uncomment and set DATABASE_URL as an env var
# DATABASE_URL = os.environ.get('DATABASE_URL')

# DATABASES = {
#     'default': dj_database_url.parse(
#         DATABASE_URL,
#         conn_max_age=600,  # Optional: Keeps connections open longer for performance
#         conn_health_checks=True,  # Optional: Enables health checks (Django 4.1+)
#     )
# }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",  # Changed from PostgreSQL
#         "NAME": "mounteve_mounteverest_summit",
#         "USER": "mounteve_rameshsah",
#         "PASSWORD": "Ramesh@5611",
#         "HOST": "localhost",
#         "PORT": "3306",  # Default MySQL port
        
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
# static root here
STATIC_ROOT = BASE_DIR / 'static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# CKEditor configuration
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',
        'toolbar': 'full',
        'height': 'auto',
        'width': 'auto',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ],
        'contentsCss': [
            '/static/css/custom_ckeditor.css',
        ],
    }
}






# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#media file here 
MEDIA_URL ='/media/'
MEDIA_ROOT = BASE_DIR /'media'   
 

AUTH_USER_MODEL = 'accounts.CustomUser'


## Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rsah3798@gmail.com'
EMAIL_HOST_PASSWORD = 'your_email_password'


# SEMANTIC_APP_LIST = [
#     {'app_label': 'accounts'},
#     {'app_label': 'news'},
#     {'app_label': 'advertising_channel'},

#     {'app_label': 'enquiry'},
#     {'app_label': 'emailnewsletter'},
#     {'app_label': 'weather'},
#     {'app_label': 'chatbot_app'},
   
  
# ]





# Cache configuration (using local memory for simplicity)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


CKEDITOR_UPLOAD_PATH = "uploads/"  # directory inside MEDIA_ROOT
CKEDITOR_IMAGE_BACKEND = "pillow"
# ==============================
# JAZZMIN ADMIN CONFIGURATION
# ==============================

JAZZMIN_SETTINGS = {
    # ---------- Branding ----------
    "site_title": "Nepal Speaks Live",
    "site_header": "NSL Admin",
    "site_brand": "Nepal Speaks Live",

    # No logo images — text only
    "login_logo": "images/mount_everest_summit_logo_width.png",
    "login_logo_dark": "images/mount_everest_summit_logo_width.png",
    "site_logo": None,
    "site_logo_classes": "fw-bold text-primary fs-4",  # styled text as logo
    "site_icon": "images/favicon.ico",

    "welcome_sign": "Welcome to Nepal Speaks Live Admin Portal",
    "copyright": "© 2025 Nepal Speaks Live Pvt. Ltd.",
    "user_avatar": None,

    # ---------- Top Menu ----------
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"], "icon": "fas fa-gauge-high"},
        {"name": "Website", "url": "/", "new_window": True, "icon": "fas fa-earth-asia"},
        {"app": "auth"},
        {"app": "news"},
        {"app": "expeditions"},
    ],

    # ---------- User Menu ----------
    "usermenu_links": [
        {"name": "Profile", "url": "admin:auth_user_change", "new_window": False, "icon": "fas fa-user-gear"},
        {"model": "auth.user"},
        {"name": "Support", "url": "mailto:support@mounteverest-summit.com", "icon": "fas fa-headset"},
    ],

    # ---------- Sidebar ----------
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": [
        "auth", "accounts", "news", "expeditions", "orders", "analytics",
        "advertising_channel", "chatbot_app", "email_newsletter", "enquiry"
    ],

    # ---------- App & Model Icons ----------
    "icons": {
        # --- Core Django ---
        "auth": "fas fa-user-shield",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-people-group",

        # --- Accounts / Users ---
        "accounts": "fas fa-id-badge",
        "accounts.CustomUser": "fas fa-user-circle",
        "accounts.Profile": "fas fa-address-card",

        # --- News / Blog ---
        "news": "fas fa-newspaper",
        "news.News": "fas fa-file-lines",
        "news.NewsCategory": "fas fa-layer-group",
        "news.NewsSubCategory": "fas fa-tags",
        "news.NewsImage": "fas fa-image",
        "news.NewsVideo": "fas fa-video",
        "news.Comment": "fas fa-comments",

        # --- Expeditions / Packages ---
        "expeditions": "fas fa-mountain-sun",
        "expeditions.Expedition": "fas fa-person-hiking",
        "expeditions.Package": "fas fa-box-open",
        "expeditions.Booking": "fas fa-calendar-check",

        # --- Orders / Payments ---
        "orders": "fas fa-cart-shopping",
        "orders.Order": "fas fa-file-invoice-dollar",
        "orders.Payment": "fas fa-credit-card",
        "orders.Invoice": "fas fa-receipt",

        # --- Analytics / Reports ---
        "analytics": "fas fa-chart-line",
        "analytics.Report": "fas fa-chart-pie",
        "analytics.Metric": "fas fa-percent",

        # --- Advertising / Marketing ---
        "advertising_channel": "fas fa-bullhorn",
        "advertising_channel.AdPlacement": "fas fa-rectangle-ad",
        "advertising_channel.AdvertisingInquiry": "fas fa-envelope-open-text",

        # --- Chatbot / Conversations ---
        "chatbot_app": "fas fa-robot",
        "chatbot_app.Conversation": "fas fa-comments",
        "chatbot_app.Message": "fas fa-message",

        # --- Email Newsletter ---
        "email_newsletter": "fas fa-envelope-circle-check",
        "email_newsletter.EmailNewsletter": "fas fa-envelope-open-text",
        "email_newsletter.EmailNewsletterSubscriber": "fas fa-envelope", 

        # --- Enquiry / Contact ---
        "enquiry": "fas fa-circle-question",
        "enquiry.Enquiry": "fas fa-inbox",

        # --- Other Django Apps ---
        "sites": "fas fa-globe",
        "sessions": "fas fa-hourglass-half",
        "admin.LogEntry": "fas fa-clock-rotate-left",
    },

    # ---------- Custom Quick Actions ----------
    "custom_links": {
        "news": [
            {
                "name": "Add News Article",
                "url": "admin:news_news_add",
                "icon": "fas fa-circle-plus",
                "permissions": ["news.add_news"],
            },
        ],
        "expeditions": [
            {
                "name": "Add Expedition",
                "url": "admin:expeditions_expedition_add",
                "icon": "fas fa-square-plus",
                "permissions": ["expeditions.add_expedition"],
            },
        ],
    },

    # ---------- UI Layout ----------
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },

    "language_chooser": True,
    "show_ui_builder": False,
}

# ==============================
# JAZZMIN UI TWEAKS (White Theme)
# ==============================

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": None,
    "navbar": "navbar-white navbar-light",
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-white elevation-1",
    "sidebar_nav_small_text": False,
    "footer_fixed": False,
    "body_small_text": False,
    "brand_colour": "navbar-white",
    "accent": "accent-info",
    "button_classes": {
        "primary": "btn btn-outline-primary",
        "secondary": "btn btn-outline-secondary",
        "info": "btn btn-outline-info",
        "warning": "btn btn-outline-warning",
        "danger": "btn btn-outline-danger",
        "success": "btn btn-outline-success",
    },
    "actions_sticky_top": True,
}



# === Wikidata Site Info ===
SITE_NAME = "Nepal Speaks Live"
SITE_ALTERNATE_NAME = "THE WORLD’S HIGHEST NEWS ROOM"
SITE_URL = "https://www.nepalspeakslive.com.np"
SITE_LOGO = "https://mounteverest-summit.com/static/images/logo.png"
SITE_DESCRIPTION = (
    "Nepal Speaks Live –  "
)
SITE_FOUNDING_DATE = "2025"

SOCIAL_LINKS = [
    "https://www.wikidata.org/wiki/Q136698656",
    "https://w.wiki/FvVc",
    "https://www.facebook.com/yourpage",
    "https://www.instagram.com/yourhandle",
    "https://www.youtube.com/yourchannel",
]

SITEMAP_URL = "https://www.nepalspeakslive.com.np/sitemap.xml"
CSRF_TRUSTED_ORIGINS = [
    "http://www.nepalspeakslive.com.np",
    "https://www.nepalspeakslive.com.np",
    "http://nepalspeakslive.com.np",
    "https://nepalspeakslive.com.np"
]


