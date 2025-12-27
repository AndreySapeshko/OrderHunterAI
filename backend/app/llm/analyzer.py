import logging

from pydantic import ValidationError

from backend.app.db.crud import activate_state
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

    async def analyze(self, lead) -> bool:
        prompt = render_messages(lead.description)
        logger.info("SART LLM analyze")

        try:
            raw = await self.llm.analyze(prompt)
            parsed = LLMLeadResult.model_validate(raw)
        except ValidationError:
            logger.exception("LLM response validation failed")
            return False
        except Exception:
            logger.exception("LLM call failed and disable")
            await activate_state("disable_llm")
            return False
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
        return True
