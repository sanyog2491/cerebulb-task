import logging
import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventory_project.settings")
logger = logging.getLogger(__name__)

app = Celery(
    "inventory_project",
    broker="amqp://",
    backend="rpc://",
    include=["apps.inventory_app.tasks"],
)


app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.beat_schedule = {
    "check-low-stock-every-night": {
        "task": "apps.inventory_app.tasks.check_low_stock",
        'schedule': crontab(hour=0, minute=0),
    },
}


app.conf.timezone = "UTC"

if __name__ == "__main__":
    app.start()
