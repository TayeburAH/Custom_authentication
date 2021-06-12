"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&7g@%cp4_a(pn-!gr5r9e4r-q!2*8c9ru6&t5gsqam0n%os$4k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#
ALLOWED_HOSTS = ['127.0.0.1:8000','authentication-my-app.herokuapp.com']

INSTALLED_APPS = [
    # 'custom_account.apps.AccountConfig',
    'custom_account',
    'django_cleanup',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # <---   Allauth  --->
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # providers
    # selected providers, more at https://django-allauth.readthedocs.io/en/latest/installation.html
    'allauth.socialaccount.providers.facebook',  # if you need FB api
    'allauth.socialaccount.providers.google',  # if you need google api

]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'custom_account.User'  # change from built-in user model to ours
# <app_name>.custom_model_name


# for capital or small letter email1234
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    # Needed to login by email_phone in Django admin, regardless of `allauth`
    'custom_account.backends.EmailOrPhoneModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Check the site ID number from admin
# Must change the site to localhost:8000/
# Must use python manage.py runserver localhost:8080
SITE_ID = 1





# ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
# SECURE_SSL_REDIRECT = True


# Settings for email as username

# By default new account is created with Username(first _name and last_name)
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False

# Create a new account which is linked to a new user in User
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'     # Don't verify the email account

# Redirect after login
LOGIN_REDIRECT_URL = '/'

# Redirect after logout
LOGOUT_REDIRECT_URL = 'http://localhost:8080/main/'

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        #'METHOD': 'js_sdk',
        #'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
    },

}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'  # Change project name

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mysite.wsgi.application'  # Change project name

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

MEDIA_URL = '/media/'  # to make a url
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# This is where we are going to upload the pictures


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Heroku runs collectstatic and puts all static files here

# point to static outside app directory
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'tayebur@canadaeducationbd.com'  # must have 'Less secure app access' turned on go to https://myaccount.google.com/u/1/security
EMAIL_HOST_PASSWORD = '687687687687'
DEFAULT_FROM_EMAIL = 'no-reply<no_reply@domain.com>'

# BASE_DIR = 'http://127.0.0.1:8000'

# After login where it should be redirected?

#
# SOCIALACCOUNT_PROVIDERS = {
#      'facebook':
#         {
#          'METHOD': 'oauth2',
#          'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
#          'SCOPE': ['email', 'public_profile'],
#          'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
#          'INIT_PARAMS': {'cookie': True},
#          'FIELDS': [
#              'id',
#              'first_name',
#              'last_name',
#              'name',
#              'name_format',
#              'picture',
#              'short_name'
#          ],
#          'EXCHANGE_TOKEN': True,
#          'LOCALE_FUNC': lambda request: 'ru_RU',
#          'VERIFIED_EMAIL': False,
#          'VERSION': 'v7.0',
#          # you should fill in 'APP' only if you don't create a Facebook instance at /admin/socialaccount/socialapp/
#          'APP': {
#              'client_id': '312607463830711',  # !!! THIS App ID
#              'secret': 'a4b002fe79cd03b0bbc01a789f571393',  # !!! THIS App Secret
#              'key': ''
#                 }
#          }
# }

