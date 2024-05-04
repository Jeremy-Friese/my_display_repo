import os
from django.utils import timezone

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
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0plmpwd3v5mhukq#tjmpc+hda8akv727ik13mf+c5#33#52p)('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS =  ["192.168.37.58", "127.0.0.1", "www.536Pollyann.com", "536Pollyann.com", "76052homes.com", "www.76052homes.com",
                    "haslethome.com", "www.haslethome.com",
                 ]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SECURE_SSL_REDIRECT_EXEMPT = ["ads"]
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_DOMAIN =  ".536Pollyann.com"
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app1',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]


SPEEDINFO_EXCLUDE_URLS = [
    r'/admin/',
    ]

ROOT_URLCONF = '536Pollyann.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = '536Pollyann.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, '/static')
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
