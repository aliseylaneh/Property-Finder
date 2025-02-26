from config.env_conf.env import env

# https://docs.celeryproject.org/en/stable/userguide/configuration.html

REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')
CELERY_BROKER_URL = 'redis://{host}:{port}/0'.format(host=REDIS_HOST, port=REDIS_PORT)
CELERY_RESULT_BACKEND = 'redis://{host}:{port}'.format(host=REDIS_HOST, port=REDIS_PORT)
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_TASK_LOCK_CACHE = "default"

CELERY_TIMEZONE = "Asia/Tehran"

CELERY_TASK_SOFT_TIME_LIMIT = 20  # seconds
CELERY_TASK_TIME_LIMIT = 30  # seconds
CELERY_TASK_MAX_RETRIES = 3

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TASK_LOCK_EXPIRE = 36000
