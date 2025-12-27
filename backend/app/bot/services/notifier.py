from backend.app.bot.services.leads_keyboard import lead_keyboard
from backend.app.db.models.lead_ai import LeadAI
from backend.app.db.models.leads import Lead


async def notify_lead(bot, chat_id: int, lead: Lead, lead_ai: LeadAI):
    text = (
        f"🤖 Новый AI-лид\n\n"
        f"📌 {lead.title}\n\n"
        f"🏷 Категория: {lead_ai.category}\n"
        f"⭐ Score: {lead_ai.score}/100\n\n"
        f"{lead.description[:500]}"
    )

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=lead_keyboard(str(lead.id)),
        disable_web_page_preview=True,
    )
