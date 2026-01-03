from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.auth.dependencies import get_current_user
from backend.app.api.schemas.lead import LeadStatusUpdate
from backend.app.api.schemas.user_lead import UserLeadOut
from backend.app.db import User, UserLead
from backend.app.db.models.leads import Lead
from backend.app.db.session import get_session

router = APIRouter()


@router.get("/", response_model=List[UserLeadOut])
async def list_user_leads(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    async with session:
        stmt = (
            select(UserLead, Lead)
            .outerjoin(Lead, Lead.id == UserLead.lead_id)
            .order_by(UserLead.created_at.desc())
            .where(UserLead.user_id == current_user.id)
            .limit(limit)
            .offset(offset)
        )

        result = await session.execute(stmt)

    items = []
    for user_lead, lead in result:
        items.append(UserLeadOut.from_orm(user_lead, lead, lead.raw_item))

    return items


@router.get("/{user_lead_id}", response_model=UserLeadOut)
async def get_user_lead(
    user_lead_id: UUID, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    async with session:
        stmt = (
            select(UserLead, Lead)
            .outerjoin(Lead, Lead.id == UserLead.lead_id)
            .where(UserLead.user_id == current_user.id, UserLead.id == user_lead_id)
        )

        result = await session.execute(stmt)
        row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Lead not found")

    user_lead, lead = row
    return UserLeadOut.from_orm(user_lead, lead, lead.raw_item)


@router.patch("/user_leads/{user_lead_id}/status", response_model=UserLeadOut)
async def update_lead_status(
    user_lead_id: UUID,
    payload: LeadStatusUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    async with session:
        stmt = (
            select(UserLead, Lead)
            .outerjoin(Lead, Lead.id == UserLead.lead_id)
            .where(UserLead.user_id == current_user.id, UserLead.id == user_lead_id)
        )

        result = await session.execute(stmt)
        row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Lead not found")

    user_lead, lead = row

    user_lead.status = payload.status
    await session.commit()
    await session.refresh(user_lead)

    return UserLeadOut.from_orm(user_lead, lead, lead.raw_item)
