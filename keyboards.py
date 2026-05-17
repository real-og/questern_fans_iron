from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def get_bot_sections_kb(sections):
    kb = InlineKeyboardMarkup(row_width=1)

    for section in sections:
        content_text = (section.content_text or "").strip()
        file_name = (section.file_name or "").strip()

        if not section.is_shown:
            continue

        if not content_text and not file_name:
            continue

        kb.add(
            InlineKeyboardButton(
                text=section.button_name,
                callback_data=str(section.section_id)
            )
        )

    if not kb.inline_keyboard:
        return None

    return kb

def get_contact_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = KeyboardButton(
        text="📱 Поделиться контактом",
        request_contact=True
    )
    kb.add(btn)
    return kb