import random
from datetime import datetime, timezone

import httpx

from backend.app.sources.base import BaseSourceConnector
from backend.app.sources.types import RawSourceItem
from backend.app.sources.user_agents import USER_AGENTS


class RedditForHireConnector(BaseSourceConnector):
    source_id = "reddit_forhire"
    source_name = "Reddit r/forhire"
    supports_cursor = True

    BASE_URL = "https://www.reddit.com/r/forhire/new.json"

    async def fetch(self, *, since=None, cursor=None, limit=50):
        params = {"limit": limit}
        if cursor:
            params["after"] = cursor

        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": ("text/html,application/xhtml+xml,application/xml;" "q=0.9,image/avif,image/webp,*/*;q=0.8"),
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        }

        async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=30) as client:
            resp = await client.get(self.BASE_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

        posts = data["data"]["children"]
        next_cursor = data["data"].get("after")

        for post in posts:
            p = post["data"]

            yield RawSourceItem(
                external_id=p["id"],
                url=f"https://reddit.com{p['permalink']}",
                title=p["title"],
                content=p.get("selftext", ""),
                author=p.get("author"),
                published_at=datetime.fromtimestamp(p["created_utc"], tz=timezone.utc),
                metadata={
                    "subreddit": p.get("subreddit"),
                    "score": p.get("score"),
                },
            )

        if next_cursor:
            await self.save_cursor(next_cursor)
