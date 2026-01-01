from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from backend.app.api.schemas.lead import LeadOut, LeadStatusUpdate
from backend.app.api.schemas.user_lead import UserLeadOut
from backend.app.db import UserLead
from backend.app.db.models.lead_ai import LeadAI
from backend.app.db.models.leads import Lead
from backend.app.db.session import async_session

router = APIRouter()


@router.get("/", response_model=List[UserLeadOut])
async def list_user_leads(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    async with async_session() as session:
        stmt = (
            select(UserLead, Lead)
            .outerjoin(Lead, Lead.id == UserLead.lead_id)
            .order_by(UserLead.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await session.execute(stmt)

    items = []
    for user_lead, lead in result:
        items.append(UserLeadOut.from_orm(user_lead, lead, lead.raw_item))

    return items


@router.get("/{user_lead_id}", response_model=UserLeadOut)
async def get_user_lead(user_lead_id: UUID):
    async with async_session() as session:
        stmt = select(UserLead, Lead).outerjoin(Lead, Lead.id == UserLead.lead_id).where(UserLead.id == user_lead_id)

        result = await session.execute(stmt)
        row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Lead not found")

    user_lead, lead = row
    return UserLeadOut.from_orm(user_lead, lead, lead.raw_item)


@router.patch("/leads/{lead_id}/status", response_model=LeadOut)
async def update_lead_status(
    lead_id: UUID,
    payload: LeadStatusUpdate,
):
    async with async_session() as session:
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
