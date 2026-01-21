from datetime import datetime

from backend.app.db.models.source_state import SourceStateModel
from backend.app.db.session import async_session


class SourceState:
    async def get_cursor(self, source_id: str) -> str | None:
        async with async_session() as session:
            state = await session.get(SourceStateModel, source_id)
            return state.cursor if state else None

    async def save_cursor(self, source_id: str, cursor: str) -> None:
        async with async_session() as session:
            state = await session.get(SourceStateModel, source_id)
            if not state:
                state = SourceStateModel(source_id=source_id)
                session.add(state)
            state.cursor = cursor
            state.last_seen_at = datetime.utcnow()
            await session.commit()

    async def mark_success(self, source_id: str) -> None:
        async with async_session() as session:
            state = await session.get(SourceStateModel, source_id)
            if state:
                state.last_success_at = datetime.utcnow()
                state.error_count = 0
                await session.commit()

    async def mark_error(self, source_id: str, error: str) -> None:
        async with async_session() as session:
            state = await session.get(SourceStateModel, source_id)
            if not state:
                state = SourceStateModel(source_id=source_id, error_count=0)
                session.add(state)
            state.error_count += 1
            state.last_error = error
            await session.commit()
