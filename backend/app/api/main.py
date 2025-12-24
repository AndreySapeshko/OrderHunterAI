import logging
import logging.config

from backend.app.api.routers import leads
from backend.app.logging_config import LOGGING_CONFIG
from backend.app.sources.registry import SourceRegistry

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

from fastapi import FastAPI

from backend.app.api.scheduler import setup_scheduler, scheduler
import backend.app.sources.connectors.registry_connectors

logger.info("Registered sources: %s",SourceRegistry.list_sources(),)

app = FastAPI(
    title="Order hunter AI",
    version="0.1.0",
)

app.include_router(leads.router, prefix="/api/leads", tags=["leads"])


@app.on_event("startup")
async def startup():
    logger.info("STARTUP: starting scheduler")
    setup_scheduler()
    if not scheduler.running:
        scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()
    logger.info("STARTUP: scheduler started")
