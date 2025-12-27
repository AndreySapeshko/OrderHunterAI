import asyncio
import json
import time

import openai
from openai import AsyncOpenAI

from backend.app.config import OPEN_AI_KEY
from backend.app.llm.client import BaseLLMClient

client = AsyncOpenAI(api_key=OPEN_AI_KEY)


class OpenAILLMClient(BaseLLMClient):
    def __init__(self, client: AsyncOpenAI, model: str = "gpt-4.1-mini", min_interval: float = 31.0):
        self.client = client
        self.model = model
        self.min_interval = min_interval
        self._last_call = 0
        self._lock = asyncio.Lock()

    async def _throttled(self):
        async with self._lock:
            now = time.time()
            delta = now - self._last_call

            if delta < self.min_interval:
                await asyncio.sleep(self.min_interval - delta)

            self._last_call = time.time()

    async def analyze(self, messages: list[dict]) -> dict:
        for attempt in range(5):
            await self._throttled()
            try:
                resp = await self.client.chat.completions.create(
                    model=self.model, messages=messages, response_format={"type": "json_object"}
                )

                content = resp.choices[0].message.content
                data = json.loads(content)
                return data

            except openai.RateLimitError:
                await asyncio.sleep(31)

        raise RuntimeError("LLM rate limit retry failed")


def get_llm_client() -> OpenAILLMClient:
    return OpenAILLMClient(client)
