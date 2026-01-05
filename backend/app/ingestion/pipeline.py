import logging
from datetime import datetime

from sqlalchemy import select

from backend.app.db.crud import get_limited_to
from backend.app.db.models.raw_items import RawItem
from backend.app.db.session import async_session
from backend.app.ingestion.dedup import compute_content_hash
from backend.app.ingestion.utils import process_created_lead
from backend.app.llm.services import process_new_lead_ai

logger = logging.getLogger(__name__)


class IngestionPipeline:
    def __init__(self, connector):
        self.connector = connector
        self.state = connector.state

    async def run(self, limit: int = 100) -> None:
        cursor = await self.connector.get_cursor()

        try:
            async for item in self.connector.fetch(cursor=cursor, limit=limit):
                await self._process_item(item)

            await self.connector.mark_success()

        except Exception as e:
            await self.connector.mark_error(str(e))
            raise

    async def _process_item(self, item):
        content = item.content
        title = item.title
        if not title and not content:
            return
        if len(content) < 200:
            return
        content_hash = compute_content_hash(title, content)

        async with async_session() as session:
            stmt = select(RawItem).where((RawItem.content_hash == content_hash))
            existing = await session.scalar(stmt)

            if existing:
                return

            raw = RawItem(
                source_id=self.connector.source_id,
                external_id=item.external_id,
                url=item.url,
                title=item.title,
                content=item.content,
                author=item.author,
                published_at=item.published_at,
                content_hash=content_hash,
                price_limit=item.metadata.get("price_limit", None),
                possible_price_limit=item.metadata.get("possible_price_limit", None),
                currency=item.metadata.get("currency", None),
            )
            session.add(raw)
            await session.flush()
            await session.commit()

            lead = await process_created_lead(raw, self.connector.source_id)

            if lead is None:
                logger.warning("SKIP (not match): id=%s title=%s", raw.id, title)
                await session.commit()
                return

            disabled_until = await get_limited_to("disable_llm")
            if disabled_until and disabled_until > datetime.utcnow():
                logger.warning("LLM disabled, skipping analysis")
                await session.commit()
                return

            await process_new_lead_ai(lead.id)
            await session.commit()
