import logging.config

from backend.app.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

from fastapi import FastAPI

app = FastAPI()
