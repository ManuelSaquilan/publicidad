from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from publicidad import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'publicidad.settings')

app = Celery('publicidad')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

