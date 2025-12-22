from backend.app.db.models.leads import Lead
from backend.app.db.session import async_session


async def load_lead(lead_id: int):
    async with async_session() as session:
        return await session.get(Lead, lead_id)
