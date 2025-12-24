import logging.config

from backend.app.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

import os

from celery import Celery
from celery.schedules import crontab

import backend.app.sources.connectors.registry_connectors

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

celery_app = Celery(
    "orderhunterai",
    broker=f"redis://:{REDIS_PASSWORD}@redis:6379/0",
    backend=f"redis://:{REDIS_PASSWORD}@redis:6379/1",
)

celery_app.conf.beat_schedule = {
    "run-source-ingestion-every-15-min": {
        "task": "backend.app.workers.tasks.run_source_ingestion",
        "schedule": crontab(minute="*/15"),
        "args": ("reddit_forhire",),
    },
}

celery_app.autodiscover_tasks([
    "backend.app.workers"
])


@celery_app.task
def ping() -> str:
    return "pong"
