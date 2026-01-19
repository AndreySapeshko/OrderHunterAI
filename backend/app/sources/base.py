from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable, Optional

from backend.app.sources.schema import RawSourceItem
from backend.app.sources.state import SourceState


class BaseSourceConnector(ABC):
    """
    Base contract for all data sources.
    """

    source_id: str  # unique key, e.g. "reddit_forhire"
    source_name: str  # human-readable
    supports_cursor: bool = True

    def __init__(self, state: SourceState):
        self.state = state

    @abstractmethod
    async def fetch(
        self,
        *,
        since: Optional[datetime] = None,
        cursor: Optional[str] = None,
        limit: int = 100,
    ) -> Iterable[RawSourceItem]:
        """
        Fetch new raw items from source.
        Must NOT return already processed items.
        """
        raise NotImplementedError

    async def get_cursor(self) -> Optional[str]:
        return await self.state.get_cursor(self.source_id)

    async def save_cursor(self, cursor: str) -> None:
        await self.state.save_cursor(self.source_id, cursor)

    async def mark_success(self) -> None:
        await self.state.mark_success(self.source_id)

    async def mark_error(self, error: str) -> None:
        await self.state.mark_error(self.source_id, error)
