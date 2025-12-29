import pytest

from pathlib import Path
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from backend.app.sources.utils import parse_kwork_projects, process_projects


def test_parse_kwork_projects_ok():
    html_file = Path(__file__).parent.parent.parent / "fixtures" / "kwork_projects.html"
    html = open(html_file, encoding="utf-8").read()

    items = list(parse_kwork_projects(html))

    assert len(items) == 1
    item = items[0]

    assert isinstance(item, dict)
    assert str(item["id"]) == "123"
    assert "Telegram бота" in item["title"]
    assert "python" in item["description"]


def test_parse_kwork_projects_empty():
    html = "<html><body>No data</body></html>"

    with pytest.raises(RuntimeError):
        list(parse_kwork_projects(html))


def test_parse_kwork_projects_keyword_filter():
    html = """
    <script>
    window.__INITIAL_STATE__ = {
      "wantsListData": {
        "pagination": {
          "data": [
            {
              "id": 1,
              "name": "Резюме разработчика",
              "description": "Составить резюме",
              "date_create": "2025-12-26 15:48:00"
            }
          ]
        }
      }
    }
    </script>
    """

    items = list(parse_kwork_projects(html))

    assert items == []


def test_parse_kwork_projects_date():
    html_file = Path(__file__).parent.parent.parent / "fixtures" / "kwork_projects.html"
    html = open(html_file, encoding="utf-8").read()
    item = list(parse_kwork_projects(html))[0]

    assert isinstance(item.get("published_at"), datetime)


@pytest.mark.asyncio
async def test_process_projects_builds_items(monkeypatch, sessionmaker):
    # is_already_saved всегда False
    monkeypatch.setattr(
        "backend.app.sources.utils.is_already_saved",
        AsyncMock(return_value=False),
    )

    # parse_kwork_date чтобы не зависеть от формата даты
    monkeypatch.setattr(
        "backend.app.sources.utils.parse_kwork_date",
        lambda _: datetime(2025, 1, 1, tzinfo=timezone.utc),
    )

    monkeypatch.setattr("backend.app.db.crud.async_session", sessionmaker)

    projects = [
        {
            "id": "123",
            "title": "Need AI chatbot",
            "description": "Looking for GPT chatbot",
            "user_id": "42",
            "username": "testuser",
            "date_create": "2025-01-01",
            "price_limit": "1000",
            "possible_price_limit": "2000",
            "category_id": 41,
            "expires_at": "2025-02-01",
            "lang": "ru",
        }
    ]

    stop, items = await process_projects(projects)

    assert stop is False
    assert len(items) == 1
    item = items[0]
    assert item.external_id == "kwork:123"
    assert item.title == "Need AI chatbot"
    assert item.content == "Looking for GPT chatbot"
    assert item.url == "https://kwork.ru/projects/123"
    assert item.metadata["category_id"] == 41


@pytest.mark.asyncio
async def test_process_projects_skips_without_id(monkeypatch, sessionmaker):
    monkeypatch.setattr(
        "backend.app.sources.utils.is_already_saved",
        AsyncMock(return_value=False),
    )
    monkeypatch.setattr(
        "backend.app.sources.utils.parse_kwork_date",
        lambda _: datetime(2025, 1, 1, tzinfo=timezone.utc),
    )

    monkeypatch.setattr("backend.app.db.crud.async_session", sessionmaker)

    projects = [
        {"title": "No id project"},  # ни id, ни wantId
        {"wantId": "W1", "title": "Has wantId", "description": "x", "date_create": "d"},
    ]

    stop, items = await process_projects(projects)

    assert stop is False
    assert len(items) == 1
    assert items[0].external_id == "kwork:W1"
    assert items[0].url == "https://kwork.ru/projects/W1"


@pytest.mark.asyncio
async def test_process_projects_stops_on_already_saved(monkeypatch, sessionmaker):
    # первый проект новый, второй "уже сохранен" -> stop_category True и второй не добавляется
    async def fake_is_saved(external_id: str) -> bool:
        return external_id == "kwork:2"

    monkeypatch.setattr(
        "backend.app.sources.utils.is_already_saved",
        AsyncMock(side_effect=fake_is_saved),
    )
    monkeypatch.setattr(
        "backend.app.sources.utils.parse_kwork_date",
        lambda _: datetime(2025, 1, 1, tzinfo=timezone.utc),
    )

    monkeypatch.setattr("backend.app.db.crud.async_session", sessionmaker)

    projects = [
        {"id": "1", "title": "first", "description": "a", "date_create": "d"},
        {"id": "2", "title": "second", "description": "b", "date_create": "d"},
        {"id": "3", "title": "third", "description": "c", "date_create": "d"},
    ]

    stop, items = await process_projects(projects)

    assert stop is True
    assert len(items) == 1
    assert items[0].external_id == "kwork:1"


@pytest.mark.asyncio
async def test_process_projects_calls_is_already_saved_with_correct_external_id(monkeypatch):
    is_saved = AsyncMock(return_value=False)
    monkeypatch.setattr(
        "backend.app.sources.utils.is_already_saved",
        is_saved,
    )
    monkeypatch.setattr(
        "backend.app.sources.utils.parse_kwork_date",
        lambda _: datetime(2025, 1, 1, tzinfo=timezone.utc),
    )

    projects = [{"wantId": "W9", "title": "x", "description": "y", "date_create": "d"}]
    await process_projects(projects)

    is_saved.assert_awaited_once_with("kwork:W9")
