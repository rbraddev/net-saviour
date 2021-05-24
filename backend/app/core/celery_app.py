import os

from celery import Celery

from app.config import CeleryConfig
from app.core.inventory.tasks import update_inventory


celery_app = Celery(__name__)

celery_app.config_from_object(CeleryConfig)

@celery_app.task(name="low_priority:update_inventory")
def update_inventory_task():
    update_inventory()