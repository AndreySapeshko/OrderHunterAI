from backend.app.bot.services.notifier import notify_lead
from backend.app.db.crud import (
    get_all_active_users_with_rules,
    get_or_create_lead_by_row_item,
    get_or_create_user_lead,
)
from backend.app.db.models.raw_items import RawItem
from backend.app.rules.engine import RuleEngine


async def process_created_lead(raw: RawItem):
    items = await get_all_active_users_with_rules()
    lead = None

    for item in items:
        user = item.get("user")
        rules = item.get("rules")
        engine = RuleEngine(rules)
        match, scor = engine.match(raw)

        if user and match:
            lead = await get_or_create_lead_by_row_item(raw)
            user_lead = await get_or_create_user_lead(user.id, lead.id, scor)
            if engine.should_notify(raw, scor):
                if user_lead.sent_to_telegram:
                    return lead
                await notify_lead(lead.id, user.chat_id, raw, scor)
                user_lead.sent_to_telegram = True

    return lead
