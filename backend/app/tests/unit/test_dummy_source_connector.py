import pytest

from backend.app.sources.connectors.dummy import DummySourceConnector
from backend.app.sources.state import SourceState
from backend.app.sources.types import RawSourceItem


@pytest.mark.asyncio
async def test_dummy_connector_fetch() -> None:
    state = SourceState()
    connector = DummySourceConnector(state=state)

    items = [item async for item in connector.fetch()]

    assert len(items) == 1
    assert isinstance(items[0], RawSourceItem)
    assert "AI agent" in items[0].content
