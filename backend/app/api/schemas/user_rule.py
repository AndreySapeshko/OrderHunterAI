from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserRuleBase(BaseModel):
    source_id: list[str] | None = None
    include_keywords: list[str] | None = None
    exclude_keywords: list[str] | None = None
    min_text_length: int = 0
    min_score: int = 0
    keyword_for_notis: list[str] | None = None
    min_score_for_notis: int = 0
    enabled: bool = True


class UserRuleCreate(UserRuleBase):
    pass


class UserRuleUpdate(UserRuleBase):
    pass


class UserRuleOut(UserRuleBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
