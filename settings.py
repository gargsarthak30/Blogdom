from django.core.urlresolvers import reverse_lazy
import os
from whitenoise import WhiteNoise
import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-rf$^(3fzvydbwi*b+t^jp*8v_%*e(t%d4$ul!ywey8k=q$5+m'

if socket.gethostname() == 'SARTHAK':
    DEBUG = True
else:
    DEBUG = False


# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'rest_framework',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blogs.apps.BlogsConfig',
    'user_account.apps.UserAccountConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blogdom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogdom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
if not DEBUG:
    DATABASES = {
        'default': {
            'HOST': 'ec2-54-243-202-110.compute-1.amazonaws.com',
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'dbj625b23toj27',
            'USER': 'zemimmeieaddkb',
            'PASSWORD': '-xfrLIaRfIDyd-mPDLTQFhjhMC',
        }
    }
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

AUTH_PROFILE_MODULE = 'userprofile.UserProfile'


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


AUTH_PROFILE_MODULE = "blogs.UserBlogdom"

LOGIN_URL = reverse_lazy('user_account.views.user_login')
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATIC_ROOT = os.path.join((BASE_DIR), 'static')
STATIC_URL = '/static/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#SMTP Configuration

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'gargsarthak30'
EMAIL_HOST_PASSWORD = 'hello123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# To send the admins mail when some server side error occurs.
ADMINS = (
    ('admin', 'admin@example.com'),
)

# For broken links.
SEND_BROKEN_LINK_EMAIL = True
MANAGERS = (
    ('admin', 'admin@example.com'),
)