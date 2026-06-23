import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ESGBack.settings")

app = Celery("ESGBack")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'repeat-parsing-every-5-mins': {
        'task': 'v1.tasks.repeat_order_make',
        'schedule': crontab(minute=5, hour=0),
    },
}
