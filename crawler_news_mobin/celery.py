import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'crawler_news_mobin.settings')

celery = Celery('crawler_news_mobin')
celery.config_from_object("django.conf:settings", namespace="CELERY")

redis_host = "redis://127.0.0.1:6379/2"
celery.conf.broker_url = redis_host
celery.conf.result_backend = redis_host
celery.autodiscover_tasks()