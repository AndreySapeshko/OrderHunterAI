import asyncio
import logging
import random

import httpx

from backend.app.sources.base import BaseSourceConnector
from backend.app.sources.state import SourceState
from backend.app.sources.utils import parse_kwork_projects, process_projects

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

    async def aclose(self):
        await self.client.aclose()

    async def fetch(self, since=None, cursor=None, limit: int = 20):
        collected = 0

        for name, category_id in CATEGORIES.items():
            if collected >= limit:
                break

            url = f"{BASE_URL}?a={category_id}"
            for page in range(1, 4):
                resp = await self.client.get(url)

                resp.raise_for_status()

                projects = parse_kwork_projects(resp.text)

                if not projects:
                    break

                stop_category, items = await process_projects(projects)

                for item in items:
                    yield item
                    collected += 1

                if stop_category:
                    break

                await asyncio.sleep(random.uniform(2.0, 4.0))

        await self.aclose()
