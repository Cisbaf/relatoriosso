from celery import Celery

app = Celery('tasks', broker='redis://redis:6379/0')
app.conf.result_backend = 'redis://redis:6379/0'
app.conf.timezone = 'UTC'

app.autodiscover_tasks(['source.infra.celery.tasks'])
