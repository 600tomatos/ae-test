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

app.conf.beat_schedule = {
    'reload-cache-every-hour': {
        'task': 'cache_loader.tasks.reload_cache',
        'schedule': 60 * 60,    # 1 hour
        'options': {'queue': 'reload_cache_queue'}
    },
}


# manual task declared in order not to wait beat 'init timeout'. Can be removed (but there will be init timeout 5 mins)
app.conf.task_routes = (
    [
        ('cache_loader.tasks.reload_cache', {'queue': 'reload_cache_queue'}),
    ],
)

