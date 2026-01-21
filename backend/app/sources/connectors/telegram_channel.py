import logging
import os
from datetime import timezone

from telethon import TelegramClient

from backend.app.sources.base import BaseSourceConnector
from backend.app.sources.schema import RawSourceItem
from backend.app.sources.state import SourceState

logger = logging.getLogger(__name__)


def extract_author(message, channel: str) -> str:
    # 1. Если есть подпись автора (каналы с signatures)
    if message.post_author:
        return message.post_author

    # 2. Если есть sender (группы, чаты)
    if message.sender:
        if getattr(message.sender, "username", None):
            return f"@{message.sender.username}"

        name = " ".join(
            filter(
                None,
                [
                    getattr(message.sender, "first_name", None),
                    getattr(message.sender, "last_name", None),
                ],
            )
        )
        if name:
            return name

    # 3. Fallback — имя канала
    return channel


class TelegramChannelConnector(BaseSourceConnector):
    source_id = "telegram_channels"
    source_name = "Telegram Channels"

    def __init__(self, state: SourceState):
        super().__init__(state)

        self.api_id = int(os.environ["TELEGRAM_API_ID"])
        self.api_hash = os.environ["TELEGRAM_API_HASH"]
        self.session = os.environ.get("TELETHON_SESSION", "tg_session")

        self.client = TelegramClient(
            self.session,
            self.api_id,
            self.api_hash,
        )

        self._started = False

        channels_raw = os.environ.get("TELEGRAM_CHANNELS", "")
        self.channels = [c.strip() for c in channels_raw.split(",") if c.strip()]

        if not self.channels:
            raise RuntimeError("TELEGRAM_CHANNELS is empty")

    async def start(self):
        if not self._started:
            await self.client.start()
            self._started = True
            logger.info("Telegram client started")

    async def stop(self):
        if self._started:
            await self.client.disconnect()
            self._started = False
            logger.info("Telegram client stopped")

    async def fetch(self, since=None, cursor=None, limit: int = 20):
        await self.start()

        for channel in self.channels:
            async for message in self.client.iter_messages(channel, limit=limit):
                if not message.text:
                    continue

                author = extract_author(message, channel)

                yield RawSourceItem(
                    external_id=str(message.id),
                    title=message.text[:80],
                    content=message.text,
                    published_at=message.date.astimezone(timezone.utc),
                    url=f"https://t.me/{channel}/{message.id}",
                    metadata={
                        "channel": channel,
                    },
                    author=author,
                )
