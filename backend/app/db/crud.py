from datetime import datetime

from asyncpg.pgproto.pgproto import timedelta
from sqlalchemy import UUID, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db import LeadSourceLink, RawItem
from backend.app.db.models.lead_ai import LeadAI
from backend.app.db.models.lead_notification import LeadNotification
from backend.app.db.models.leads import Lead
from backend.app.db.models.system_state import SystemState
from backend.app.db.models.user import User
from backend.app.db.models.user_lead import UserLead
from backend.app.db.models.user_rule import UserRule
from backend.app.db.session import async_session


async def load_lead(lead_id: int):
    async with async_session() as session:
        return await session.get(Lead, lead_id)


async def get_notified_user_ids(lead_id: UUID) -> set[UUID]:
    async with async_session() as session:
        result = await session.execute(select(LeadNotification.user_id).where(LeadNotification.lead_id == lead_id))
        return {row[0] for row in result}


async def get_lead_ai(lead_id: int):
    async with async_session() as session:
        return await session.get(LeadAI, lead_id)


async def get_all_users():
    async with async_session() as session:
        result = await session.scalars(select(User))
        return result.all()


async def get_rules_user(user_id: UUID):
    async with async_session() as session:
        return await session.get(User, user_id)


async def get_all_active_users_with_rules():
    async with async_session() as session:
        stmt = (
            select(User, UserRule)
            .outerjoin(UserRule, (UserRule.user_id == User.id) & (UserRule.enabled.is_(True)))
            .where(User.is_active.is_(True))
            .where(User.chat_id.isnot(None))
        )

        result = await session.execute(stmt)

    users_map: dict[UUID, dict] = {}

    for user, rules in result:
        if user.id not in users_map:
            users_map[user.id] = {"user": user, "rules": []}
        if rules:
            users_map[user.id]["rules"].append(rules)

    return list(users_map.values())


async def create_lead_notification(lead_id: UUID, user_id: UUID):
    async with async_session() as session:
        lead_notification = LeadNotification(lead_id=lead_id, user_id=user_id)
        session.add(lead_notification)
        await session.commit()
    return lead_notification


async def get_or_create_user_lead(user_id: UUID, lead_id: UUID, scor: int):
    async with async_session() as session:
        stmt = select(UserLead).where(
            UserLead.user_id == user_id,
            UserLead.lead_id == lead_id,
        )
        existing = await session.scalar(stmt)
        if existing:
            return existing

        user_lead = UserLead(lead_id=lead_id, user_id=user_id, heuristic_score=scor)
        session.add(user_lead)
        await session.commit()
    return user_lead


async def get_or_create_lead_by_row_item(raw: RawItem):
    async with async_session() as session:
        stmt = select(Lead).where(Lead.raw_item_id == raw.id)
        lead = (await session.scalars(stmt)).one_or_none()
        if lead:
            return lead

        lead = Lead(raw_item_id=raw.id)
        session.add(lead)
        await session.flush()

        lead_source_link = LeadSourceLink(
            lead_id=lead.id,
            raw_item_id=raw.id,
        )
        session.add(lead_source_link)
        await session.commit()

        return lead


async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    username: str | None,
) -> User:
    stmt = select(User).where(User.chat_id == telegram_id)
    user = (await session.scalars(stmt)).one_or_none()

    if user:
        # обновляем username, если изменился
        if user.username != username:
            user.username = username
        return user

    # создаём нового пользователя
    user = User(chat_id=telegram_id, username=username, password_hash="password_hash", email="test@tester.ru")
    session.add(user)
    await session.flush()

    return user


async def is_already_saved(external_id: str):
    async with async_session() as session:
        stmt = select(RawItem).where(RawItem.external_id == external_id)
        raw_item = (await session.scalars(stmt)).one_or_none()
        if raw_item:
            return True
        return False


async def activate_state(name_state: str, client_id: str, ttl_hours: int = 1):
    async with async_session() as session:
        stmt = select(SystemState).where(SystemState.name == name_state, SystemState.value == client_id)
        state = (await session.scalars(stmt)).one_or_none()

        if not state:
            state = SystemState(name=name_state, value=client_id)
            session.add(state)
            await session.flush()

        state.limited_to = datetime.utcnow() + timedelta(hours=ttl_hours)

        await session.commit()


async def get_limited_to(name_state: str, client_id: str):
    async with async_session() as session:
        stmt = select(SystemState).where(SystemState.name == name_state, SystemState.value == client_id)
        state = (await session.scalars(stmt)).one_or_none()
        return state.limited_to if state else None


async def get_user_by_email(email, session):
    stmt = select(User).where(User.email == email)
    return (await session.scalars(stmt)).one_or_none()
