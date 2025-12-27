import asyncio

from backend.app.bot.bot import bot
from backend.app.bot.services.notifier import notify_lead
from backend.app.db import Lead, LeadAI
from backend.app.db.crud import create_lead_notification, get_all_active_users_with_rules, get_notified_user_ids
from backend.app.rules.engine import RuleEngine


async def notification_sender(lead: Lead, lead_ai: LeadAI):
    items = await get_all_active_users_with_rules()
    notified_user_ids = await get_notified_user_ids(lead.id)

    tasks = []

    for item in items:
        user = item["user"]
        rules = item["rules"]
        engine = RuleEngine(rules)

        if user and engine.match(lead, lead_ai) and user.id not in notified_user_ids:
            await create_lead_notification(lead_id=lead.id, user_id=user.id)
            tasks.append(notify_lead(bot, user.chat_id, lead, lead_ai))

    if tasks:
        await asyncio.gather(*tasks)
