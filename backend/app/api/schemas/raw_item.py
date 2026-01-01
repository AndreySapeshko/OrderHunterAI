from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class RawItemListOut(BaseModel):
    id: UUID
    title: str
    content: str
    source_id: str
    published_at: datetime

    @classmethod
    def from_orm(cls, raw_item):
        return cls(
            id=raw_item.id,
            title=raw_item.title,
            content=raw_item.content,
            source_id=raw_item.source_id,
            published_at=raw_item.published_at,
        )


class RawItemOut(BaseModel):
    title: str
    content: str
    source_id: str
    published_at: datetime
    external_id: str
    url: str
    author: str
    price_limit: int | None
    possible_price_limit: int | None
    currency: str | None
    fetched_at: datetime

    @classmethod
    def from_orm(cls, raw_item):
        return cls(
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
        )
