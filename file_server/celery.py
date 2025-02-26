# file_server/file_server/celery.py
from __future__ import absolute_import
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_server.settings')

app = Celery('file_server')

# Load config from Django settings, using the CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Add a simple test task
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    return "Debug task completed"