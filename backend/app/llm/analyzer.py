import logging

import openai
from pydantic import ValidationError

from backend.app.db import Lead, RawItem
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

    async def analyze(self, lead: Lead, raw: RawItem) -> bool:
        message = render_messages(raw.content, self.llm.prompt)
        logger.info(f"START LLM analyze with {self.llm.client_id}")

        try:
            raw = await self.llm.analyze(message)
            parsed = LLMLeadResult.model_validate(raw)

        except ValidationError:
            logger.exception(f"LLM {self.llm.client_id} response validation failed")
            return False

        except openai.RateLimitError:
            logger.warning("Rate limit, temporary")
            return False  # не отключаем

        except Exception:
            logger.exception("LLM call failed and disable")
            await activate_state("disable_llm", self.llm.client_id)
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
        logger.info(
            "LLM success",
            extra={
                "client": self.llm.client_id,
                "model": self.model,
                "prompt": self.prompt_version,
            },
        )
        return True
