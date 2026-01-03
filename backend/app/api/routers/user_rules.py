from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.auth.dependencies import get_current_user
from backend.app.api.schemas.user_rule import UserRuleCreate, UserRuleOut, UserRuleUpdate
from backend.app.db import User, UserRule
from backend.app.db.session import get_session

router = APIRouter()


@router.get("/", response_model=list[UserRuleOut])
async def list_rules(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    async with session:
        stmt = select(UserRule).where(UserRule.user_id == current_user.id)
        result = await session.scalars(stmt)
        return result.all()


@router.post("/", response_model=UserRuleOut)
async def create_rule(
    data: UserRuleCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    async with session:
        rule = UserRule(**data.dict(), user_id=current_user.id)
        session.add(rule)
        await session.commit()
        await session.refresh(rule)
        return rule


@router.patch("/{rule_id}", response_model=UserRuleOut)
async def update_rule(
    rule_id: UUID,
    data: UserRuleUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    async with session:
        rule = await session.get(UserRule, rule_id)

        if not rule or rule.user_id != current_user.id:
            raise HTTPException(status_code=404)

        for k, v in data.dict(exclude_unset=True).items():
            setattr(rule, k, v)

        await session.commit()
        return rule


@router.delete("/{rule_id}")
async def delete_rule(
    rule_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    async with session:
        rule = await session.get(UserRule, rule_id)

        if not rule or rule.user_id != current_user.id:
            raise HTTPException(status_code=404)

        await session.delete(rule)
        await session.commit()

    return {"ok": True}
