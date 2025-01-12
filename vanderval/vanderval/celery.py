from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vanderval.settings')

# Create Celery application
app = Celery('vanderval')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in all installed apps
app.autodiscover_tasks()
