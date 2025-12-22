import pytest

from backend.app.sources.base import BaseSourceConnector
from backend.app.sources.state import SourceState


class TestConnector(BaseSourceConnector):
    source_id = "test"
    source_name = "Test"

    async def fetch(self, *, since=None, cursor=None, limit=100):
        return []


@pytest.mark.asyncio
async def test_base_connector_cursor_methods(sessionmaker, monkeypatch) -> None:
    monkeypatch.setattr("backend.app.sources.state.async_session", sessionmaker)
    state = SourceState()
    connector = TestConnector(state=state)

    assert await connector.get_cursor() is None

    await connector.save_cursor("abc")
    assert await connector.get_cursor() == "abc"


@pytest.mark.asyncio
async def test_base_connector_mark_error_and_success(sessionmaker, monkeypatch) -> None:
    monkeypatch.setattr("backend.app.sources.state.async_session", sessionmaker)
    state = SourceState()
    connector = TestConnector(state=state)

    await connector.mark_error("failed")
    await connector.mark_success()

    # Проверяем, что вызовы не падают
    assert True
