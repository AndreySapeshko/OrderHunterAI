from sqlalchemy import UUID, select

from backend.app.db.models.lead_ai import LeadAI
from backend.app.db.models.lead_notification import LeadNotification
from backend.app.db.models.leads import Lead
from backend.app.db.models.user import User
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
