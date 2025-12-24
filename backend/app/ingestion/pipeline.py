from sqlalchemy import select

from backend.app.db.models.lead_source_links import LeadSourceLink
from backend.app.db.models.leads import Lead
from backend.app.db.models.raw_items import RawItem
from backend.app.db.session import async_session
from backend.app.ingestion.dedup import compute_content_hash
from backend.app.llm.services import process_new_lead


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
        content_hash = compute_content_hash(item.title, item.content)

        async with async_session() as session:
            # 1. exact dedup
            stmt = select(RawItem).where((RawItem.content_hash == content_hash))
            existing = await session.scalar(stmt)

            if existing:
                return  # уже видели

            # 2. save raw_item
            raw = RawItem(
                source_id=self.connector.source_id,
                external_id=item.external_id,
                url=item.url,
                title=item.title,
                content=item.content,
                author=item.author,
                published_at=item.published_at,
                content_hash=content_hash,
            )
            session.add(raw)
            await session.flush()

            # 3. create draft lead
            lead = Lead(
                title=item.title,
                description=item.content,
            )
            session.add(lead)
            await session.flush()

            await process_new_lead(lead.id)

            # 4. link
            session.add(
                LeadSourceLink(
                    lead_id=lead.id,
                    raw_item_id=raw.id,
                )
            )

            await session.commit()
