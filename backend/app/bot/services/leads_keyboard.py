from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def lead_keyboard(lead_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Save", callback_data=f"lead_action:{lead_id}:save"),
                InlineKeyboardButton(text="❌ Reject", callback_data=f"lead_action:{lead_id}:reject"),
            ],
            [
                InlineKeyboardButton(text="🟡 In Progress", callback_data=f"lead_action:{lead_id}:progress"),
            ],
        ]
    )
