import logging

from pydantic import ValidationError

from backend.app.db.models.lead_ai import LeadAI
from backend.app.db.session import async_session
from backend.app.llm.schemas import LLMLeadResult
from backend.app.llm.utils import render_messages

logger = logging.getLogger(__name__)


class LeadAnalyzer:
    def __init__(self, llm_client, prompt_version: str):
        self.llm = llm_client
        self.model = llm_client.model
        self.prompt_version = prompt_version

    async def analyze(self, lead):
        prompt = render_messages(lead.description)
        raw = await self.llm.analyze(prompt)

        try:
            parsed = LLMLeadResult.model_validate(raw)
        except ValidationError:
            logger.exception("Analyzer failed")
            raise
        extracted = parsed.model_dump(
            exclude={
                "is_relevant",
                "category",
                "score",
            }
        )
        ai = LeadAI(
            lead_id=lead.id,
            is_relevant=parsed.is_relevant,
            category=parsed.category,
            extracted=extracted,
            score=parsed.score,
            model=self.model,
            prompt_version=self.prompt_version,
        )

        async with async_session.begin() as session:
            await session.merge(ai)
