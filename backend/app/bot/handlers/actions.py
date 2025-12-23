from aiogram import F, Router
from aiogram.types import CallbackQuery

from backend.app.core.enums import LeadStatus
from backend.app.db.models.leads import Lead
from backend.app.db.session import async_session

router = Router()


@router.callback_query(F.data.startswith("lead_action:"))
async def handle_lead_action(callback: CallbackQuery):
    _, lead_id, action = callback.data.split(":")

    async with async_session() as session:
        lead = await session.get(Lead, lead_id)

        if action == "save":
            lead.status = LeadStatus.SAVED
        elif action == "reject":
            lead.status = LeadStatus.REJECTED
        elif action == "progress":
            lead.status = LeadStatus.IN_PROGRESS

        await session.commit()

    await callback.answer("Готово")
    await callback.message.edit_reply_markup()
