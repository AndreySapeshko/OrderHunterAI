from unittest.mock import AsyncMock

import pytest

from backend.app.llm.registry import ClientRegistry
from backend.app.llm.services import process_new_lead_ai
from backend.app.tests.mocks.fake_llm import get_fake_client


@pytest.mark.asyncio
async def test_process_new_lead_calls_notification(mocker, sessionmaker, monkeypatch):
    monkeypatch.setattr("backend.app.db.crud.async_session", sessionmaker)
    ClientRegistry.register(get_fake_client())

    lead_id = "123"

    mocker.patch("backend.app.llm.services.load_lead", return_value=mocker.Mock(id=lead_id))

    analyzer = mocker.patch(
        "backend.app.llm.services.LeadAnalyzer",
        autospec=True,
    )
    analyzer.return_value.analyze = AsyncMock(return_value=True)

    await process_new_lead_ai(lead_id)

    analyzer.assert_called_once()
