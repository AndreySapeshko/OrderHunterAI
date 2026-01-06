from datetime import datetime, timezone

import pytest

from backend.app.sources.connectors.reddit_forhire import RedditForHireConnector
from backend.app.sources.state import SourceState


@pytest.mark.asyncio
async def test_reddit_connector_parses_items(mocker):
    fake_response = {
        "data": {
            "children": [
                {
                    "data": {
                        "id": "abc123",
                        "title": "Need AI chatbot",
                        "selftext": "Looking for GPT chatbot",
                        "author": "testuser",
                        "created_utc": 1700000000,
                        "permalink": "/r/forhire/test",
                        "score": 10,
                        "subreddit": "forhire",
                    }
                }
            ],
            "after": None,
        }
    }

    mocker.patch(
        "httpx.AsyncClient.get",
        return_value=mocker.Mock(
            json=lambda: fake_response,
            raise_for_status=lambda: None,
        ),
    )

    connector = RedditForHireConnector(state=SourceState())

    items = []
    async for item in connector.fetch():
        items.append(item)

    assert len(items) == 1
    item = items[0]

    assert item.external_id == "abc123"
    assert "AI chatbot" in item.title
    assert item.published_at == datetime.fromtimestamp(1700000000, tz=timezone.utc)
