from backend.app.bot.bot import bot
from backend.app.bot.services.leads_keyboard import lead_keyboard
from backend.app.db import RawItem
from backend.app.db.models.lead_ai import LeadAI


async def notify_lead(lead_id: str, chat_id: int, raw: RawItem, score: int, lead_ai: LeadAI = None):
    ai_score = lead_ai.score if lead_ai else ""
    category = lead_ai.category if lead_ai else ""
    text = (
        f"🆕 * Новый лид *\n\n"
        f"📌 {raw.title}\n\n"
        f"💰 {raw.price_limit}–{raw.possible_price_limit}\n"
        f"⭐ Score: {score}/7\n\n"
        f"{raw.content[:500]}\n\n"
        f"🤖 AI-анализ:\n\n"
        f"⭐ Score: {ai_score}/7\n\n"
        f"✔️ Категория: {category}"
    )

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=lead_keyboard(str(lead_id)),
        disable_web_page_preview=True,
    )
