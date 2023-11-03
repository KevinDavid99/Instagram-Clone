"""
Django settings for Instagramclone project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from rest_framework.settings import api_settings
import os
from pathlib import Path
import cloudinary
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x(65#7r%-nqw+pz&cu@_=^h!p7cdq@ej&cvgi_977i$8hqvh2p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False 

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'knox',
    'rest_framework',
    'instaclone',
    'users',
    'corsheaders',
]


AUTH_USER_MODEL = 'instaclone.User'


CORS_ALLOWED_ORIGINS = [
    'https://kem-instagram-clone.netlify.app',
    'https://kem-instagram-clone.onrender.com'
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'knox.auth.TokenAuthentication',   
    )
}


# REST_KNOX = {
#     'SECURE_HASH_ALGORITHM':'cryptography.hazmat.primitives.hashes.SHA512',
#     'AUTH_TOKEN_CHARACTER_LENGTH': 64, # By default, it is set to 64 characters (this shouldn't need changing).
#     'TOKEN_TTL': timedelta(minutes=1), # The default is 10 hours i.e., timedelta(hours=10)).
#     'USER_SERIALIZER': 'knox.serializers.UserSerializer',
#     'TOKEN_LIMIT_PER_USER': None, # By default, this option is disabled and set to None -- thus no limit.
#     'AUTO_REFRESH': False, # This defines if the token expiry time is extended by TOKEN_TTL each time the token is used.
#     'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
# }





MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]

ROOT_URLCONF = 'Instagramclone.urls'

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

WSGI_APPLICATION = 'Instagramclone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'InstagramCloneDB',
#         'USER': 'postgres',
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }   

import dj_database_url

DATABASES = {
    'default' : dj_database_url.parse(os.environ.get('RENDER_EXT_DB_URL'))
}




# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'


cloudinary.config(
    cloud_name = os.environ.get('CLOUD_NAME'),
    api_key = os.environ.get('API_KEY'),
    api_secret = os.environ.get('API_SECRET'),
    secure = True
)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'



# Default primary key field type  
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
