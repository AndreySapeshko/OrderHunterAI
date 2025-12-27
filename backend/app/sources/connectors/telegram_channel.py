import os
from datetime import timezone

from telethon import TelegramClient

from backend.app.sources.base import BaseSourceConnector
from backend.app.sources.selection_parameters import KEYWORDS_TELEGRAM, MIN_TEXT_LENGTH, STOP_WORDS
from backend.app.sources.state import SourceState
from backend.app.sources.types import RawSourceItem


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

        channels_raw = os.environ.get("TELEGRAM_CHANNELS", "")
        self.channels = [c.strip() for c in channels_raw.split(",") if c.strip()]

        if not self.channels:
            raise RuntimeError("TELEGRAM_CHANNELS is empty")

    async def fetch(self, since=None, cursor=None, limit: int = 20):
        async with TelegramClient(
            self.session,
            self.api_id,
            self.api_hash,
        ) as client:
            for channel in self.channels:
                async for message in client.iter_messages(channel, limit=limit):
                    if not message.text:
                        continue

                    text = message.text.lower()

                    if len(text) < MIN_TEXT_LENGTH:
                        continue

                    if any(sw in text for sw in STOP_WORDS):
                        continue

                    if not any(k in text for k in KEYWORDS_TELEGRAM):
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
