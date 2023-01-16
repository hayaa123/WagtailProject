from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d&-e4mj(0jv!x%%fsk=3dp*je929pcv6l!xly!a-b3c%1t^&2v'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions", 
    ]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

INTERNAL_IPS = ('127.0.0.1','127.17.0.1')

try:
    from .local import *
except ImportError:
    pass
