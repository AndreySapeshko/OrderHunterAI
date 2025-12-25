from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import func, select

from backend.app.db.models.leads import Lead
from backend.app.db.models.raw_items import RawItem
from backend.app.ingestion.pipeline import IngestionPipeline
from backend.app.sources.connectors.dummy import DummySourceConnector
from backend.app.sources.state import SourceState


@pytest.mark.asyncio
async def test_ingestion_idempotent(session, sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.ingestion.pipeline.async_session", sessionmaker)
    monkeypatch.setattr("backend.app.sources.state.async_session", sessionmaker)
    monkeypatch.setattr("backend.app.llm.analyzer.async_session", sessionmaker)
    monkeypatch.setattr("backend.app.db.crud.async_session", sessionmaker)
    with (patch("backend.app.ingestion.pipeline.process_new_lead", new_callable=AsyncMock),):
        state = SourceState()
        connector = DummySourceConnector(state=state)
        pipeline = IngestionPipeline(connector)

        await pipeline.run()
        await pipeline.run()  # повтор

        raw_count = await session.scalar(select(func.count()).select_from(RawItem))
        lead_count = await session.scalar(select(func.count()).select_from(Lead))

        assert raw_count == 1
        assert lead_count == 1
