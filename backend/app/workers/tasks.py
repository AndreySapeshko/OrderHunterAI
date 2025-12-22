from backend.app.api.celery_app import celery_app
from backend.app.ingestion.pipeline import IngestionPipeline
from backend.app.sources.registry import SourceRegistry
from backend.app.sources.state import SourceState


@celery_app.task
def run_source_ingestion(source_id: str):
    state = SourceState()
    connector_cls = SourceRegistry.get(source_id)
    connector = connector_cls(state=state)

    pipeline = IngestionPipeline(connector)
    return pipeline.run()
