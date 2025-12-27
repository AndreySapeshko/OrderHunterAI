import asyncio
import logging
import random
import httpx

from backend.app.db.crud import is_already_saved
from backend.app.sources.base import BaseSourceConnector
from backend.app.sources.selection_parameters import KEYWORDS_TELEGRAM
from backend.app.sources.state import SourceState
from backend.app.sources.types import RawSourceItem
from backend.app.sources.utils import parse_kwork_date, parse_kwork_projects

logger = logging.getLogger(__name__)


BASE_URL = "https://kwork.ru/projects"

CATEGORIES = {
    "programming": 41,
    "chatbots": 170,
    "automation": 174,
}


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}


class KworkProjectsConnector(BaseSourceConnector):
    source_id = "kwork_projects"
    source_name = "Kwork Projects"

    def __init__(self, state: SourceState):
        super().__init__(state)
        self.client = httpx.AsyncClient(headers=HEADERS, timeout=30)

    async def fetch(self, since=None, cursor=None, limit: int = 20):
        collected = 0

        for name, category_id in CATEGORIES.items():
            if collected >= limit:
                break

            url = f"{BASE_URL}?a={category_id}"
            stop_category = False
            for page in range(1, 4):
                resp = await self.client.get(url)

                resp.raise_for_status()

                projects = parse_kwork_projects(resp.text)

                if not projects:
                    break

                for project in projects[:limit]:
                    if await is_already_saved(f"kwork:{project.get("id", "")}"):
                        stop_category = True
                        break

                    project_id = project.get("id") or project.get("wantId")
                    if not project_id:
                        continue

                    content = project.get("description", "").lower()
                    matched = [k for k in KEYWORDS_TELEGRAM if k.lower() in content]
                    if not matched:
                        logger.info("SKIP (no keywords): id=%s title=%s", project.get("id"), project.get("title"))
                        continue

                    yield RawSourceItem(
                        external_id=f"kwork:{project.get("id", "")}",
                        title=project.get("title", ""),
                        content=content,
                        author=f"kwork id:{project.get("user_id", "")} username: {project.get("username", "unknown")}",
                        published_at=parse_kwork_date(project.get("date_create")),
                        url=f"https://kwork.ru/projects/{project.get("id")}",
                        metadata={
                            "price_limit": project.get("price_limit", ""),
                            "possible_price_limit": project.get("possible_price_limit", ""),
                            "category_id": project.get("category_id"),
                            "expires_at": project.get("expires_at"),
                            "lang": project.get("lang"),
                        },
                    )
                    collected += 1

                if stop_category:
                    break

                # анти-бан пауза
                await asyncio.sleep(random.uniform(2.0, 4.0))
