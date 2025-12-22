from backend.app.sources.base import BaseSourceConnector
from backend.app.sources.types import RawSourceItem


class DummySourceConnector(BaseSourceConnector):
    source_id = "dummy"
    source_name = "Dummy Source"

    async def fetch(self, *, since=None, cursor=None, limit=100):
        yield RawSourceItem(
            external_id="1",
            url="https://example.com",
            title="Test AI Agent Project",
            content="Looking for AI agent developer",
            author="tester",
            published_at=None,
            metadata={},
        )
