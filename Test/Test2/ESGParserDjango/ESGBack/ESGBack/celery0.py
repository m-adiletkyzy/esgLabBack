import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ESGBack.settings")
app = Celery("ESGBack")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# заносим таски в очередь
app.conf.beat_schedule = {
    'every night': {
        'task': 'v1.tasks.parse_websites',
        'schedule': crontab(minute=5, hour=0),
    },
    #'test': {
    #'task': 'v1.tasks.parse_test',
    #'schedule': crontab(),
    #},

}

#Worker
# celery -A ESGBack worker -E -l INFO -P solo

# beat cmd
# celery -A ESGBack beat --pidfile=celerybeat.pid -l INFO
