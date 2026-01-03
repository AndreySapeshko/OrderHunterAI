import logging
import logging.config

from starlette.middleware.cors import CORSMiddleware

from backend.app.api.routers import admin, auth, leads, raw_items, user_leads, user_rules
from backend.app.logging_config import LOGGING_CONFIG
from backend.app.sources.registry import SourceRegistry

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

from fastapi import FastAPI

import backend.app.sources.connectors.registry_connectors
from backend.app.api.scheduler import scheduler, setup_scheduler

logger.info(
    "Registered sources: %s",
    SourceRegistry.list_sources(),
)

app = FastAPI(
    title="Order hunter AI",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leads.router, prefix="/api/leads", tags=["leads"])
app.include_router(user_leads.router, prefix="/api/user_leads", tags=["user_leads"])
app.include_router(raw_items.router, prefix="/api/raw_items", tags=["raw_items"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(user_rules.router, prefix="/api/user_rules", tags=["rules"])


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
