from .base import *

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

DEBUG = False

ALLOWED_HOSTS = ['*']
