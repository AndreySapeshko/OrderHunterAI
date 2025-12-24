from sqlalchemy import UUID

from backend.app.bot.services.sender import notification_sender
from backend.app.db.crud import load_lead, get_lead_ai
from backend.app.llm.analyzer import LeadAnalyzer
from backend.app.llm.openai_client import get_llm_client


async def process_new_lead(lead_id: UUID):
    lead = await load_lead(lead_id)

    analyzer = LeadAnalyzer(
        llm_client=get_llm_client(),
        prompt_version="v1",
    )

    if not await analyzer.analyze(lead):
        return

    lead_ai = await get_lead_ai(lead.id)

    if lead_ai and lead_ai.is_relevant:
        await notification_sender(lead, lead_ai)