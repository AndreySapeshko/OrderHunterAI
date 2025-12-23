import asyncio
import logging

from backend.app.api.celery_app import celery_app
from backend.app.bot.bot import bot
from backend.app.bot.services.notifier import notify_lead
from backend.app.db.crud import (
    create_lead_notification,
    get_all_active_users_with_rules,
    get_lead_ai,
    get_notified_user_ids,
    load_lead,
)
from backend.app.db.models.lead_ai import LeadAI
from backend.app.db.models.leads import Lead
from backend.app.ingestion.pipeline import IngestionPipeline
from backend.app.llm.analyzer import LeadAnalyzer
from backend.app.llm.openai_client import get_llm_client
from backend.app.rules.engine import RuleEngine
from backend.app.sources.registry import SourceRegistry
from backend.app.sources.state import SourceState

logger = logging.getLogger(__name__)


@celery_app.task
def run_source_ingestion(source_id: str):
    state = SourceState()
    connector_cls = SourceRegistry.get(source_id)
    connector = connector_cls(state=state)

    pipeline = IngestionPipeline(connector)
    return pipeline.run()


@celery_app.task
def analyze_lead(lead_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(analyze_lead_async(lead_id))
    except Exception:
        logger.info("Failed analyze_lead task")
    finally:
        loop.close()


async def analyze_lead_async(lead_id):
    lead = await load_lead(lead_id)
    analyzer = LeadAnalyzer(llm_client=get_llm_client(), prompt_version="v1")

    if not await analyzer.analyze(lead):
        return lead_id

    lead_ai = await get_lead_ai(lead.id)

    if lead_ai and lead_ai.is_relevant:
        await notification_sender(lead, lead_ai)

    return lead_id


async def notification_sender(lead: Lead, lead_ai: LeadAI):
    items = await get_all_active_users_with_rules()
    notified_user_ids = await get_notified_user_ids(lead.id)

    tasks = []

    for item in items:
        user = item["user"]
        rules = item["rules"]
        engine = RuleEngine(rules)

        if engine.match(lead, lead_ai) and user.id not in notified_user_ids:
            await create_lead_notification(lead_id=lead.id, user_id=user.id)
            tasks.append(notify_lead(bot, user.chat_id, lead, lead_ai))

    if tasks:
        await asyncio.gather(*tasks)
