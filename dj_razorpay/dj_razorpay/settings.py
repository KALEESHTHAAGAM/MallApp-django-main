"""
Django settings for dj_razorpay project.

Generated by 'django-admin startproject' using Django 4.2.6.

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
SECRET_KEY = 'django-insecure-#*%1v!xs@60&a@miv-ensjw$a&(w3@=av=@x(etau&@ga#$v#v'
RAZOR_KEY_ID = 'rzp_test_2h8n68Dp5BnsgZ'

RAZOR_KEY_SECRET = 'RadEymMn08SuR4yGSXsvp4qJ'





# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.19','127.0.0.1','localhost', 'http://127.0.0.1:4040' ,' modest-wondrous-starling.ngrok-free.app' ,'https://ff6d-27-4-243-84.ngrok-free.app']


# Application definition

INSTALLED_APPS = [
    'payment',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',  
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

CSRF_COOKIE_SECURE = True
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['X-CSRFToken']

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


DATA_UPLOAD_MAX_MEMORY_SIZE = 40 * 1024 * 1024  # Set the limit to 10MB (adjust as needed)


CORS_ALLOWED_ORIGINS = [
    'http://192.168.166.200:8081',  # Add the origin of your React Native app
]
ROOT_URLCONF = 'dj_razorpay.urls'

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

WSGI_APPLICATION = 'dj_razorpay.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
      'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'mallbackend',
    'HOST': 'localhost',
    'PORT': 3306,   
    'USER': 'root',
},
#    'mongodb': {
#     'ENGINE': 'djongo',
#     'ENFORCE_SCHEMA': False,  
#     'NAME': 'mall_app',
#     'HOST': 'mongodb://localhost:27017/',
#     'PORT': 27017,   
#     'USER': 'kaleesh',
#     'PASSWORD': 'kaleesh6383',
#     'AUTH_SOURCE': 'kaleesh@',
# }
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
AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',
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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'payment.UserProfile'