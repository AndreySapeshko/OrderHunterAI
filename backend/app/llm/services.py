from sqlalchemy import UUID

from backend.app.db.crud import load_lead
from backend.app.llm.analyzer import LeadAnalyzer
from backend.app.llm.openai_client import get_llm_client


async def process_new_lead_ai(lead_id: UUID):
    lead = await load_lead(lead_id)

    analyzer = LeadAnalyzer(
        llm_client=get_llm_client(),
        prompt_version="v1",
    )

    await analyzer.analyze(lead, lead.raw_item)
