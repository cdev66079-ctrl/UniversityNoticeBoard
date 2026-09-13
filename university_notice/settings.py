"""
Django settings for university_notice project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# ==========================================================
# SECURITY
# ==========================================================

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY is not configured.")

DEBUG = os.getenv(
    "DJANGO_DEBUG",
    "True"
).lower() == "true"
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "192.168.3.27"
]


# ==========================================================
# APPLICATIONS
# ==========================================================

INSTALLED_APPS = [

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Our apps
    'notices',
]


# ==========================================================
# MIDDLEWARE
# ==========================================================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==========================================================
# URL CONFIGURATION
# ==========================================================

ROOT_URLCONF = 'university_notice.urls'


# ==========================================================
# TEMPLATES
# ==========================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'notices.context_processors.notifications',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ==========================================================
# WSGI
# ==========================================================

WSGI_APPLICATION = 'university_notice.wsgi.application'


# ==========================================================
# DATABASE
# ==========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv(
            "DB_NAME",
            "university_notice_board"
        ),
        "USER": os.getenv(
            "DB_USER",
            "root"
        ),
        "PASSWORD": os.getenv(
            "DB_PASSWORD"
        ),
        "HOST": os.getenv(
            "DB_HOST",
            "127.0.0.1"
        ),
        "PORT": os.getenv(
            "DB_PORT",
            "3306"
        ),
        "OPTIONS": {
            "charset": "utf8mb4",
            "ssl": True,
        },
    }
}

if not os.getenv("DB_PASSWORD"):
    raise ValueError("DB_PASSWORD is not configured.")

# ==========================================================
# PASSWORD VALIDATION
# ==========================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==========================================================
# LANGUAGE / TIMEZONE
# ==========================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True


# ==========================================================
# STATIC FILES
# ==========================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


# ==========================================================
# MEDIA / UPLOADED FILES
# ==========================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================================
# DEFAULT PRIMARY KEY
# ==========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================================
# EMAIL
# ==========================================================

EMAIL_BACKEND = (
    'django.core.mail.backends.console.EmailBackend'
)
