from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import buttons


menu_kb = ReplyKeyboardMarkup(
    [
        [buttons.scheadule, buttons.guide],
        [buttons.sales, buttons.maps],
        [buttons.schema, buttons.infocatalog],
        [buttons.activity, buttons.my_number]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)



def get_contact_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = KeyboardButton(
        text="📱 Поделиться контактом",
        request_contact=True
    )
    kb.add(btn)
    return kb

def get_agree_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(
            text="✅ Согласен",
            callback_data='agree'
        )
    )
    return kb
