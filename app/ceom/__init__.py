from __future__ import absolute_import
from .celery import app as celery_app, test_shared_tasks

__all__ = ('celery_app',)

test_shared_tasks.delay()