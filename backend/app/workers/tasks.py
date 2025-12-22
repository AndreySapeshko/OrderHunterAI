import asyncio

from backend.app.api.celery_app import celery_app
from backend.app.db.crud import load_lead
from backend.app.ingestion.pipeline import IngestionPipeline
from backend.app.llm.analyzer import LeadAnalyzer
from backend.app.llm.openai_client import get_llm_client
from backend.app.sources.registry import SourceRegistry
from backend.app.sources.state import SourceState


@celery_app.task
def run_source_ingestion(source_id: str):
    state = SourceState()
    connector_cls = SourceRegistry.get(source_id)
    connector = connector_cls(state=state)

    pipeline = IngestionPipeline(connector)
    return pipeline.run()


@celery_app.task
def analyze_lead(lead_id):
    return asyncio.run(analyze_lead_async(lead_id))


async def analyze_lead_async(lead_id):
    lead = await load_lead(lead_id)
    analyzer = LeadAnalyzer(llm_client=get_llm_client(), prompt_version="v1")
    return await analyzer.analyze(lead)
