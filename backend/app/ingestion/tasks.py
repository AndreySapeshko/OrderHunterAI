import logging

from backend.app.ingestion.pipeline import IngestionPipeline
from backend.app.sources.registry import SourceRegistry
from backend.app.sources.state import SourceState

logger = logging.getLogger(__name__)


async def run_source_ingestion(source_id: str):
    state = SourceState()
    connector_cls = SourceRegistry.get(source_id)
    connector = connector_cls(state=state)
    pipeline = IngestionPipeline(connector)
    try:
        await pipeline.run()
    finally:
        if source_id == "telegram_channels":
            await connector.stop()


async def run_all_sources():
    logger.info("ENTER run_all_sources task")
    for source_id in SourceRegistry.list_sources():
        logger.info(f"run_source_ingestion with: {source_id}")
        try:
            await run_source_ingestion(source_id)
        except Exception:
            logger.exception("Source %s failed", source_id)
    logger.info("EXIT run_all_sources")
