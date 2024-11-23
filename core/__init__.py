# django_project/_init_.py
from .celery import app as celery_app

_all_ = ('celery_app',)

default_app_config = 'core.apps.CoreConfig'