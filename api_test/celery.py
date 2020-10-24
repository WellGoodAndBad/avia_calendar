from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_test.settings')
app = Celery('api_test')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'parse-data': {
        'task': 'api_test_work.tasks.parse_task',
        'schedule': crontab(minute='*/120'),
    },
    'check-data': {
        'task': 'api_test_work.tasks.checking_task',
        'schedule': crontab(minute='*/180'),
    },
    'parse-data_midnigth': {
        'task': 'api_test_work.tasks.parse_task',
        'schedule': crontab(minute=0, hour=0),
    },
}