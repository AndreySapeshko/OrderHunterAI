from unittest.mock import AsyncMock, patch

import pytest

from backend.app.db.crud import get_lead_ai
from backend.app.llm.registry import ClientRegistry
from backend.app.llm.services import process_new_lead_ai
from backend.app.tests.mocks.fake_llm import get_fake_client


@pytest.mark.asyncio
async def test_analyze_lead_async_analysis_failed(lead, sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.db.crud.async_session", sessionmaker)
    with (
        patch("backend.app.llm.services.load_lead", return_value=lead),
        patch("backend.app.llm.services.LeadAnalyzer.analyze", new_callable=AsyncMock, return_value=False),
    ):
        await process_new_lead_ai(lead.id)

        assert await get_lead_ai(lead.id) is None


@pytest.mark.asyncio
async def test_analyze_lead_async_not_relevant(lead, lead_ai_not_relevant, sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.db.crud.async_session", sessionmaker)
    with (
        patch("backend.app.llm.services.load_lead", return_value=lead),
        patch("backend.app.llm.services.LeadAnalyzer.analyze", new_callable=AsyncMock, return_value=True),
    ):
        await process_new_lead_ai(lead.id)

        assert await get_lead_ai(lead.id) is None


@pytest.mark.asyncio
async def test_analyze_lead_async_happy_path(lead, lead_ai_relevant, sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.db.crud.async_session", sessionmaker)
    ClientRegistry.register(get_fake_client())
    with (
        patch("backend.app.llm.services.load_lead", return_value=lead),
        patch("backend.app.llm.services.LeadAnalyzer.analyze", new_callable=AsyncMock, return_value=True) as analyzer,
    ):
        await process_new_lead_ai(lead.id)

        analyzer.assert_awaited_once()
