from offlinedatacollector.settings.staging import *   # noqa

# There should be only minor differences from staging

DATABASES['default']['NAME'] = 'offlinedatacollector_production'
DATABASES['default']['USER'] = 'offlinedatacollector_production'

EMAIL_SUBJECT_PREFIX = '[Offlinedatacollector Prod] '

# Uncomment if using celery worker configuration
# BROKER_URL = 'amqp://offlinedatacollector_production:%(BROKER_PASSWORD)s@%(BROKER_HOST)s/offlinedatacollector_production' % os.environ  # noqa
