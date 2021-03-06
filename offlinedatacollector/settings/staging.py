from offlinedatacollector.settings.base import *  # noqa

os.environ.setdefault('CACHE_HOST', '127.0.0.1:11211')
os.environ.setdefault('BROKER_HOST', '127.0.0.1:5672')

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default']['NAME'] = 'offlinedatacollector_staging'
DATABASES['default']['USER'] = 'offlinedatacollector_staging'
DATABASES['default']['HOST'] = os.environ.get('DB_HOST', '')
DATABASES['default']['PORT'] = os.environ.get('DB_PORT', '')
DATABASES['default']['PASSWORD'] = os.environ['DB_PASSWORD']

WEBSERVER_ROOT = '/var/www/offlinedatacollector/'

PUBLIC_ROOT = os.path.join(WEBSERVER_ROOT, 'public')

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

LOGGING['handlers']['file']['filename'] = os.path.join(
    WEBSERVER_ROOT, 'log', 'offlinedatacollector.log')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '%(CACHE_HOST)s' % os.environ,
    }
}

EMAIL_SUBJECT_PREFIX = '[Offlinedatacollector Staging] '

COMPRESS_ENABLED = True

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(';')

# Uncomment if using celery worker configuration
# CELERY_SEND_TASK_ERROR_EMAILS = True
# BROKER_URL = 'amqp://offlinedatacollector_staging:%(BROKER_PASSWORD)s@%(BROKER_HOST)s/offlinedatacollector_staging' % os.environ  # noqa
