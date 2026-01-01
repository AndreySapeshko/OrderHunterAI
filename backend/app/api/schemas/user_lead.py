from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from backend.app.api.schemas.lead import LeadOut
from backend.app.api.schemas.raw_item import RawItemOut
from backend.app.core.enums import LeadStatus


class UserLeadOut(BaseModel):
    id: UUID
    lead_id: UUID
    heuristic_score: int
    sent_to_telegram: bool
    status: str
    created_at: datetime

    lead: Optional[LeadOut]
    raw_item: Optional[RawItemOut]

    @classmethod
    def from_orm(cls, user_lead, lead, raw_item):
        return cls(
            id=user_lead.id,
            lead_id=user_lead.lead_id,
            heuristic_score=user_lead.heuristic_score,
            created_at=user_lead.created_at,
            sent_to_telegram=user_lead.sent_to_telegram,
            status=user_lead.status,
            lead=LeadOut(id=lead.id, raw_item_id=lead.raw_item_id, created_at=lead.created_at),
            raw_item=RawItemOut(
                title=raw_item.title,
                content=raw_item.content,
                source_id=raw_item.source_id,
                published_at=raw_item.published_at,
                external_id=raw_item.external_id,
                url=raw_item.url,
                author=raw_item.author,
                price_limit=raw_item.price_limit,
                possible_price_limit=raw_item.possible_price_limit,
                currency=raw_item.currency,
                fetched_at=raw_item.fetched_at,
            ),
        )


class LeadStatusUpdate(BaseModel):
    status: LeadStatus
