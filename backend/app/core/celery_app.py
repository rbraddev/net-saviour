import os

from celery import Celery

from app.config import CeleryConfig



celery_app = Celery(__name__)

celery_app.config_from_object(CeleryConfig)