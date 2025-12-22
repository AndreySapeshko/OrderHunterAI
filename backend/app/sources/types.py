from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass(slots=True)
class RawSourceItem:
    external_id: Optional[str]
    url: Optional[str]
    title: str
    content: str
    author: Optional[str]
    published_at: Optional[datetime]
    metadata: Dict[str, Any]
