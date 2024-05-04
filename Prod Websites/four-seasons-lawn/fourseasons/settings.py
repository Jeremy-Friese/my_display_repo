import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
FONTS_DIR = os.path.join(BASE_DIR, "templates/fonts")
HTML_DIR = os.path.join(BASE_DIR, "templates/html")
CSS_DIR = os.path.join(BASE_DIR, "templates/css")
JS_DIR = os.path.join(BASE_DIR, "templates/js")
PICS_DIR = os.path.join(BASE_DIR, "templates/pics")
MEDIA_DIR = os.path.join(BASE_DIR, "templates/media")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rs_s+o^vhvku-b*ynkjz-!ze0l87_^e(nf_wv9)u^!9qwx0c^h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["192.168.37.58", "192.168.86.23", "myfourseasonslawn.com", "myfourseasonslawn.com", "www.myfourseasonslawn.com",
                    "fsLawns.eba-4ppkig7m.us-east-1.elasticbeanstalk.com",]

if DEBUG:
    ALLOWED_HOSTS.append("127.0.0.1")

# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_user_agents',
    'django_webp',
    'speedinfo',
#    "djstripe",
    'main',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'speedinfo.middleware.ProfilerMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
]

SPEEDINFO_EXCLUDE_URLS = [
    r'/admin/',
    ]

SPEEDINFO_REPORT_COLUMNS = (
    'view_name', 'method', 'anon_calls_ratio', 'cache_hits_ratio',
    'sql_count_per_call', 'sql_time_ratio', 'total_calls', 'time_per_call', 'total_time'
)

CACHES = {
    "default": {
        "BACKEND": "speedinfo.backends.proxy_cache",
        "CACHE_BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
    }
}

SPEEDINFO_STORAGE = "speedinfo.storage.cache.storage.CacheStorage"

#SPEEDINFO_CACHE_STORAGE_CACHE_ALIAS = "speedinfo-storage"

ROOT_URLCONF = 'fourseasons.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,
        HTML_DIR,
        CSS_DIR,
        JS_DIR,
        PICS_DIR,
        MEDIA_DIR,
        FONTS_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_webp.context_processors.webp',
            ],
        },
    },
]

WSGI_APPLICATION = 'fourseasons.wsgi.application'

GZIP_CONTENT_TYPES = (
    'text/css',
    'application/javascript',
    'application/x-javascript',
    'text/javascript'
)

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY", "<your publishable key>")
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "<your secret key>")
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "pk_test_ePsdLy6kGzH4YgrmFjtY0SFx00iqXmY3iY")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "sk_test_un1SKYnxqrXaZWMKcvIGGnq500vXt7UtV4")
STRIPE_LIVE_MODE = False  # Change to True in production
DJSTRIPE_WEBHOOK_SECRET = "whsec_xxx"


STRIPE_SECRET_KEY = 'sk_test_un1SKYnxqrXaZWMKcvIGGnq500vXt7UtV4'
STRIPE_PUBLISHABLE_KEY = 'pk_test_ePsdLy6kGzH4YgrmFjtY0SFx00iqXmY3iY'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:
   STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATIC_ROOT = 'static'
STATICFILES_DIRS = [
    TEMPLATE_DIR,
    HTML_DIR,
    CSS_DIR,
    JS_DIR,
    PICS_DIR,
    MEDIA_DIR,
    FONTS_DIR,
    ]
