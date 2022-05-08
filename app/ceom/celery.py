from __future__ import absolute_import
import os

from celery import Celery, shared_task
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ceom.settings")

app = Celery("ceom")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #This import has to be done when this function gets called, otherwise it is a circular import. 
    #This file runs update_datasets in tasks_periodic.py below. Tasks_periodic.py needs to import the above app variable. Circular.
    try:
        from ceom.celeryq.tasks_periodic import update_datasets, update_rasters, clear_modis_csvs

        #Note: Errors here will not print. You will need to try/except and manually print the error

        sender.add_periodic_task(crontab(minute=1, hour=7, day_of_week='saturday'), update_datasets.s(), name='Dataset update')

        sender.add_periodic_task(crontab(minute=1, hour=7, day_of_week='sunday'), update_rasters.s(), name='Raster update')

        sender.add_periodic_task(crontab(minute=0), clear_modis_csvs.s(), name='Clear csvs')
    except Exception as e:
        print("ER?", e)
    