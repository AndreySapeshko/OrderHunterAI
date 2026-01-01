from unittest.mock import AsyncMock, patch

import pytest

from backend.app.llm.services import process_new_lead_ai


@pytest.mark.asyncio
async def test_analyze_lead_async_analysis_failed(lead):
    with (
        patch("backend.app.llm.services.load_lead", return_value=lead),
        patch("backend.app.llm.services.LeadAnalyzer.analyze", new_callable=AsyncMock, return_value=False),
        patch("backend.app.llm.services.notification_sender", new_callable=AsyncMock) as notify_mock,
        # patch("backend.app.llm.services.get_lead_ai", return_value=lead_ai),
    ):
        await process_new_lead_ai(lead.id)

        notify_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_analyze_lead_async_not_relevant(lead, lead_ai_not_relevant):
    with (
        patch("backend.app.llm.services.load_lead", return_value=lead),
        patch("backend.app.llm.services.LeadAnalyzer.analyze", new_callable=AsyncMock, return_value=True),
        patch("backend.app.llm.services.get_lead_ai", return_value=lead_ai_not_relevant),
        patch("backend.app.llm.services.notification_sender", new_callable=AsyncMock) as notify_mock,
    ):
        await process_new_lead_ai(lead.id)

        notify_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_analyze_lead_async_happy_path(lead, lead_ai_relevant):
    with (
        patch("backend.app.llm.services.load_lead", return_value=lead),
        patch("backend.app.llm.services.LeadAnalyzer.analyze", new_callable=AsyncMock, return_value=True) as analyzer,
        patch("backend.app.llm.services.get_lead_ai", return_value=lead_ai_relevant),
    ):
        await process_new_lead_ai(lead.id)

        analyzer.assert_awaited_once()
