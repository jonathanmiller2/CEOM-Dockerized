from __future__ import absolute_import
import os

from celery import Celery, shared_task
from celery.schedules import crontab
from ceom.celeryq.tasks_periodic import update_datasets

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ceom.settings")

app = Celery("ceom")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@shared_task(bind=True)
def test_shared_tasks(self):
    print('Shared tasks are working') #TODO: This still needs to be tested. Does this task have to run before MODIS tasks work?

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0, hour=3, day_of_week='sunday'), update_datasets.s(), name='Weekly dataset update')