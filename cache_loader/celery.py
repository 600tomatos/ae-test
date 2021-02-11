from celery import Celery


REDIS_URL = 'redis://redis:6379'
BROKER_DB = '0'
RESULT_BACKEND_DB = '1'
PRIMARY_CACHE_DB = '2'
BUFFER_CACHE_DB = '3'

app = Celery(main='cache_loader')

app.conf.imports = 'cache_loader.tasks'
app.conf.broker_url = f'{REDIS_URL}/{BROKER_DB}'
app.conf.result_backend = f'{REDIS_URL}/{RESULT_BACKEND_DB}'

# TODO: fix schedule
app.conf.beat_schedule = {
    'reload-cache-every-hour': {
        'task': 'cache_loader.tasks.reload_cache',
        'schedule': 3600,
        'options': {'queue': 'reload_cache_queue'}
    },
}

