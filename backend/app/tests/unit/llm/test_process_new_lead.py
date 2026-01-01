from unittest.mock import AsyncMock

import pytest

from backend.app.llm.services import process_new_lead_ai


@pytest.mark.asyncio
async def test_process_new_lead_calls_notification(mocker):
    lead_id = "123"

    mocker.patch("backend.app.llm.services.load_lead", return_value=mocker.Mock(id=lead_id))

    analyzer = mocker.patch(
        "backend.app.llm.services.LeadAnalyzer",
        autospec=True,
    )
    analyzer.return_value.analyze = AsyncMock(return_value=True)

    mocker.patch(
        "backend.app.llm.services.get_lead_ai",
        return_value=mocker.Mock(is_relevant=True),
    )

    await process_new_lead_ai(lead_id)

    analyzer.assert_called_once()
