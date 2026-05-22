from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import buttons


menu_kb = ReplyKeyboardMarkup([[buttons.scheadule], [buttons.points], [buttons.sales], [buttons.schema]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)



def get_contact_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = KeyboardButton(
        text="📱 Поделиться контактом",
        request_contact=True
    )
    kb.add(btn)
    return kb
