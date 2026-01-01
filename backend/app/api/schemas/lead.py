from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from backend.app.core.enums import LeadStatus


class LeadAIOut(BaseModel):
    is_relevant: bool
    category: str
    score: int
    extracted: dict


class LeadOut(BaseModel):
    id: UUID
    raw_item_id: UUID
    created_at: datetime

    ai: Optional[LeadAIOut] = None

    @classmethod
    def from_orm(cls, lead, lead_ai):
        return cls(
            id=lead.id,
            raw_item_id=lead.raw_item_id,
            created_at=lead.created_at,
            ai=(
                LeadAIOut(
                    is_relevant=lead_ai.is_relevant,
                    category=lead_ai.category,
                    score=lead_ai.score,
                    extracted=lead_ai.extracted,
                )
                if lead_ai
                else None
            ),
        )


class LeadStatusUpdate(BaseModel):
    status: LeadStatus
