from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from backend.app.db import UserRule
from backend.app.ingestion.pipeline import IngestionPipeline


@pytest.mark.asyncio
async def test_pipeline_calls_process_new_lead(mocker, sessionmaker, monkeypatch, session, test_user):
    monkeypatch.setattr("backend.app.ingestion.pipeline.async_session", sessionmaker)
    monkeypatch.setattr("backend.app.sources.state.async_session", sessionmaker)
    monkeypatch.setattr("backend.app.llm.analyzer.async_session", sessionmaker)
    monkeypatch.setattr("backend.app.db.crud.async_session", sessionmaker)

    fake_item = SimpleNamespace(
        source_id="reddit_forhire",
        external_id="1",
        url="https://reddit.com/r/forhire/test",
        title="Need AI chatbot",
        content="Looking for AI agent developer Looking for AI agent developer AI agent developer "
        "Looking for AI agent developer Looking for AI agent developer AI agent developer "
        "Looking for AI agent developer Looking for AI agent developer AI agent developer",
        author="testuser",
        published_at=datetime.now(tz=timezone.utc),
        metadata={},
    )

    rule = UserRule(user_id=test_user.id, include_keywords="agent")
    session.add(rule)
    await session.commit()

    async def fake_fetch(*args, **kwargs):
        yield fake_item

    fake_connector = mocker.Mock(
        source_id="reddit_forhire",
    )
    fake_connector.get_cursor = AsyncMock(return_value=None)
    fake_connector.fetch = fake_fetch

    fake_connector.mark_success = AsyncMock()
    fake_connector.mark_error = AsyncMock()

    pipeline = IngestionPipeline(fake_connector)

    process_mock = mocker.patch(
        "backend.app.ingestion.pipeline.process_new_lead_ai",
        new_callable=AsyncMock,
    )

    await pipeline.run()

    process_mock.assert_awaited_once()
