from typing import List

from fastapi import APIRouter, Query
from sqlalchemy import select

from backend.app.api.schemas.raw_item import RawItemListOut
from backend.app.db import RawItem
from backend.app.db.session import async_session

router = APIRouter()


@router.get("/", response_model=List[RawItemListOut])
async def list_raw_items(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    async with async_session() as session:
        stmt = select(RawItem).order_by(RawItem.fetched_at.desc()).limit(limit).offset(offset)

        result = await session.execute(stmt)
        raw_items = result.scalars().all()

    items = []
    for raw_item in raw_items:
        items.append(RawItemListOut.from_orm(raw_item))

    return items
