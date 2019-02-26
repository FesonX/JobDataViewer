"""
Django settings for JobDataViewer project.

Generated by 'django-admin startproject' using Django 1.11.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uf!(rzo!%h^+u)$&4tvu@=5t(2e_n=&q)_9qh&1tenu6$a2_h%'

# SECURITY WARNING: don't run witrh debug turned on in production!
DEBUG = True

# If U use CVM like Tencent Cloud Server, you should add CVM public ip
# in ALLOWED_HOST like ALLOWED_HOSTS = ['123.567']
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'viewer',
    'blog',
    'account',
    'article',
    'image',
    'sorl.thumbnail',
]

INTERNAL_IPS = ("127.0.0.1",)

DEBUG_TOOLBAR_CONFIG = {'JQUERY_URL': r"/static/JS/jquery-2.1.4.min.js"}


# DEBUG_TOOLBAR_MONGO_STACKTRACES = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'JobDataViewer.urls'

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

WSGI_APPLICATION = 'JobDataViewer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': None,
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 连接mongodb数据库
from mongoengine import connect
# ip地址、端口、账号、密码、账号配置数据库、验证方式
# connect('project', host='localhost', port=27017, username='xxxx', password='xxxxx', authentication_source='admin', authentication_mechanism='SCRAM-SHA-1')
# Connect Local Database
connect('Spider')


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Configure Redirect url
LOGIN_REDIRECT_URL = '/home/'

# Config Email
EMAIL_HOST = 'smtp.qq.com'
EMAIL_HOST_USER = '******'
EMAIL_HOST_PASSWORD = '******'
EMAIL_PORT = 25

# EMAIL_USE_TLS = False
EMAIL_USE_TTL = True
DEFAULT_FROM_EMAIL = "******"

# Config Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Image Configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
