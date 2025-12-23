from unittest.mock import AsyncMock, patch

import pytest

from backend.app.workers.tasks import analyze_lead_async


@pytest.mark.asyncio
async def test_analyze_lead_async_analysis_failed(lead):
    with (
        patch("backend.app.workers.tasks.load_lead", return_value=lead),
        patch("backend.app.workers.tasks.LeadAnalyzer.analyze", new_callable=AsyncMock, return_value=False),
        patch("backend.app.workers.tasks.notification_sender", new_callable=AsyncMock) as notify_mock,
    ):
        await analyze_lead_async(lead.id)

        notify_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_analyze_lead_async_not_relevant(lead, lead_ai_not_relevant):
    with (
        patch("backend.app.workers.tasks.load_lead", return_value=lead),
        patch("backend.app.workers.tasks.LeadAnalyzer.analyze", new_callable=AsyncMock, return_value=True),
        patch("backend.app.workers.tasks.get_lead_ai", return_value=lead_ai_not_relevant),
        patch("backend.app.workers.tasks.notification_sender", new_callable=AsyncMock) as notify_mock,
    ):
        await analyze_lead_async(lead.id)

        notify_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_analyze_lead_async_happy_path(lead, lead_ai_relevant):
    with (
        patch("backend.app.workers.tasks.load_lead", return_value=lead),
        patch("backend.app.workers.tasks.LeadAnalyzer.analyze", new_callable=AsyncMock, return_value=True),
        patch("backend.app.workers.tasks.get_lead_ai", return_value=lead_ai_relevant),
        patch("backend.app.workers.tasks.notification_sender", new_callable=AsyncMock) as notify_mock,
    ):
        await analyze_lead_async(lead.id)

        notify_mock.assert_awaited_once()
