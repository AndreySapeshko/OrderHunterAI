import logging
from datetime import datetime

from sqlalchemy import UUID

from backend.app.db.crud import get_limited_to, load_lead
from backend.app.llm.analyzer import LeadAnalyzer
from backend.app.llm.registry import ClientRegistry

logger = logging.getLogger(__name__)


async def process_new_lead_ai(lead_id: UUID):
    lead = await load_lead(lead_id)

    for client in ClientRegistry.list_clients():
        disabled_until = await get_limited_to("disable_llm", client.client_id)
        if disabled_until and disabled_until > datetime.utcnow():
            continue
        logger.info(f"ENTR process_new_lead_ai with: {client.client_id}")

        prompt_version = f"{client.prompt=}".split("=")[0]

        analyzer = LeadAnalyzer(
            llm_client=client,
            prompt_version=prompt_version,
        )
        is_created_lead_ai = await analyzer.analyze(lead, lead.raw_item)

        if is_created_lead_ai:
            return
    logger.info("All LLM clients disabled")
