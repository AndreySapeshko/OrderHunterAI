from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.schemas.lead import LeadOut, LeadStatusUpdate
from backend.app.db.models.lead_ai import LeadAI
from backend.app.db.models.leads import Lead
from backend.app.db.session import get_session

router = APIRouter()


@router.get("/", response_model=List[LeadOut])
async def list_leads(
    limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_session)
):
    async with session:
        stmt = (
            select(Lead, LeadAI)
            .outerjoin(LeadAI, LeadAI.lead_id == Lead.id)
            .order_by(Lead.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await session.execute(stmt)

    items = []
    for lead, lead_ai in result:
        items.append(LeadOut.from_orm(lead, lead_ai))

    return items


@router.get("/{lead_id}", response_model=LeadOut)
async def get_lead(lead_id: UUID, session: AsyncSession = Depends(get_session)):
    async with session:
        stmt = select(Lead, LeadAI).outerjoin(LeadAI, LeadAI.lead_id == Lead.id).where(Lead.id == lead_id)

        result = await session.execute(stmt)
        row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead, lead_ai = row
    return LeadOut.from_orm(lead, lead_ai)


@router.patch("/{lead_id}/status", response_model=LeadOut)
async def update_lead_status(lead_id: UUID, payload: LeadStatusUpdate, session: AsyncSession = Depends(get_session)):
    async with session:
        lead = await session.get(Lead, lead_id)

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        lead.status = payload.status
        await session.commit()
        await session.refresh(lead)

        # подтягиваем AI-данные
        stmt = select(Lead, LeadAI).outerjoin(LeadAI, LeadAI.lead_id == Lead.id).where(Lead.id == lead_id)
        result = await session.execute(stmt)
        lead, lead_ai = result.first()

    return LeadOut.from_orm(lead, lead_ai)
