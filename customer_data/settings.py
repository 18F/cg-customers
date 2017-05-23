"""
Django settings for customer_data project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import re

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import dj_database_url

from django.utils.crypto import get_random_string

# Make Cloud Foundry VCAP environment variables accessible
# https://github.com/jmcarp/py-cfenv
from cfenv import AppEnv
env = AppEnv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', True) != "False"
DEBUG_LOGS = os.environ.get('DEBUG_LOGS', True) != "False"

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'packages.apps.PackagesConfig',
    'projects.apps.ProjectsConfig',
    'customer_admin.apps.CustomerAdminConfig',
    'iaa.apps.IaaConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'uaa_client',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'uaa_client.middleware.UaaRefreshMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'customer_data.urls'

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

WSGI_APPLICATION = 'customer_data.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
database_url = os.environ.get('DATABASE_URL', 'postgres://localhost:5432/customer_data')
cf_db = env.get_service(name=re.compile('customer-db'))
if cf_db and cf_db.credentials['uri']:
    database_url = cf_db.credentials['uri']
    print('Using database instance `customer-db`')

DATABASES = {
    'default': dj_database_url.parse(database_url)
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_string(50)
django_creds = env.get_service(name=re.compile('customer-django-creds'))
if django_creds and django_creds.credentials['SECRET_KEY']:
    SECRET_KEY = django_creds.credentials['SECRET_KEY']
    print('Using UPS creds instance `customer-django-creds`')


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

AUTHENTICATION_BACKENDS = (
    'uaa_client.authentication.UaaBackend',
)

if DEBUG or DEBUG_LOGS:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'uaa_client': {
                'handlers': ['console'],
                'level': 'INFO',
            }
        }
    }

ALLOWED_HOSTS = ['localhost'] + env.uris

cf_s3 = env.get_service(name=re.compile('customer-s3'))
if cf_s3:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = cf_s3.credentials['bucket']
    AWS_S3_REGION_NAME = cf_s3.credentials['region']
    AWS_ACCESS_KEY_ID = cf_s3.credentials['access_key_id']
    AWS_SECRET_ACCESS_KEY = cf_s3.credentials['secret_access_key']
    print('Using S3 instance `customer-s3`')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_URL = 'uaa_client:login'

LOGIN_REDIRECT_URL = '/django-admin'

if DEBUG:
    UAA_AUTH_URL = 'fake:'

    UAA_TOKEN_URL = 'fake:'
else:
    UAA_AUTH_URL = 'https://login.fr.cloud.gov/oauth/authorize'

    UAA_TOKEN_URL = 'https://uaa.fr.cloud.gov/oauth/token'

uaa_service = env.get_service(name='customer-uaa-creds')
if uaa_service is not None:
    UAA_CLIENT_ID = uaa_service.credentials['UAA_CLIENT_ID']
    UAA_CLIENT_SECRET = uaa_service.credentials['UAA_CLIENT_SECRET']
    print('Using UPS creds instance `customer-uaa-creds`')
else:
    UAA_CLIENT_ID = os.environ.get('UAA_CLIENT_ID', 'client-id')
    UAA_CLIENT_SECRET = os.environ.get('UAA_CLIENT_SECRET', 'secret-string')
