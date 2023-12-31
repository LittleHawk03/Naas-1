"""
Django settings for naas_project project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)86!&+v6+yd!6sq5z2x=22(zbxq-4-81634x%yxph8(zz*#9nb'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'goldf55f@gmail.com'
EMAIL_HOST_PASSWORD = 'mngijizoxlwdatfw'  # os.environ['password_key'] suggested
EMAIL_USE_TLS = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0','localhost','127.0.0.1','116.103.226.93','*']


# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'notification_channel',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'naas_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'naas_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


def verified(user):
    print("step-change-1")
    user.active = True
    
def verified_channel(channel):
    print("step-change-2")
    channel.isSubscribed = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_VERIFIED_CALLBACK = verified
CHANNEL_VERIFIED_CALLBACK= verified_channel

EMAIL_FROM_ADDRESS = 'goldf55f@gmail.com'

# this is for the active user
EMAIL_MAIL_SUBJECT = 'VIETTEL CLOUD - Confirm your email {{ user.username }}'
EMAIL_MAIL_HTML = 'mail.html'
EMAIL_MAIL_PLAIN = 'plainmail.txt'
EMAIL_MAIL_PAGE = 'confirm.html'
EMAIL_MAIL_PAGE_TEMPLATE = 'confirm.html'

#this is for actice channel

EMAIL_CHANNEL_SUBJECT = 'VIETTEL CLOUD NAAS - Confirm your notification channel {{ channel.name }}'
EMAIL_CHANNEL_HTML = 'mail_channel.html'
EMAIL_CHANNEL_PLAIN = 'plainmail_channel.txt'
EMAIL_CHANNEL_PAGE = 'confirm_channel.html'


# cbpamuevasnbbnrb
# EMAIL_PASSWORD = 'mngijizoxlwdatfw'
EMAIL_MAIL_TOKEN_LIFE = 60 * 60
EMAIL_CHANNEL_TOKEN_LIFE = 60 * 80

EMAIL_PAGE_DOMAIN = 'http://0.0.0.0:8000/api/comfirm/email/'
CHANNEL_PAGE_DOMAIN = 'http://0.0.0.0:8000/api/comfirm/channel/'








































# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'goldf55f@gmail.com'
# EMAIL_HOST_PASSWORD = 'mngijizoxlwdatfw'  # os.environ['password_key'] suggested
# EMAIL_USE_TLS = True
