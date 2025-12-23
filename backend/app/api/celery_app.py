import logging.config

from backend.app.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

import os

from celery import Celery

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

celery_app = Celery(
    "orderhunterai",
    broker=f"redis://:{REDIS_PASSWORD}@redis:6379/0",
    backend=f"redis://:{REDIS_PASSWORD}@redis:6379/1",
)


@celery_app.task
def ping() -> str:
    return "pong"
