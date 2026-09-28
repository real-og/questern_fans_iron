from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import buttons


menu_kb = ReplyKeyboardMarkup(
    [
        [buttons.scheadule],
        [buttons.schema],
        [buttons.infocatalog],
        [buttons.maps],
        # [buttons.transfer],
        # [buttons.guide],
        # [buttons.docs],
        [buttons.sales],
        [buttons.activity],
        [buttons.lectory],
        [buttons.my_number],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

b_1 = InlineKeyboardButton('РЕГИСТРАЦИЯ', callback_data='111')
b_2 = InlineKeyboardButton('РЕГИСТРАЦИЯ', callback_data='222')
b_3 = InlineKeyboardButton('РЕГИСТРАЦИЯ', callback_data='333')
b_4 = InlineKeyboardButton('РЕГИСТРАЦИЯ', callback_data='444')
b_5 = InlineKeyboardButton('РЕГИСТРАЦИЯ', callback_data='555')
kb_lectory_1 = InlineKeyboardMarkup()
kb_lectory_1.add(b_1)
kb_lectory_2 = InlineKeyboardMarkup()
kb_lectory_2.add(b_2)
kb_lectory_3 = InlineKeyboardMarkup()
kb_lectory_3.add(b_3)
kb_lectory_4 = InlineKeyboardMarkup()
kb_lectory_4.add(b_4)
kb_lectory_5 = InlineKeyboardMarkup()
kb_lectory_5.add(b_5)




b_1 = InlineKeyboardButton('РЕГИСТРАЦИЯ', callback_data='1')
b_2 = InlineKeyboardButton('РЕГИСТРАЦИЯ', callback_data='2')
b_3 = InlineKeyboardButton('РЕГИСТРАЦИЯ', callback_data='3')
b_4 = InlineKeyboardButton('РЕГИСТРАЦИЯ', callback_data='4')
b_5 = InlineKeyboardButton('РЕГИСТРАЦИЯ', callback_data='5')
reg_kb_1 = InlineKeyboardMarkup()
reg_kb_1.add(b_1)
reg_kb_2 = InlineKeyboardMarkup()
reg_kb_2.add(b_2)
reg_kb_3 = InlineKeyboardMarkup()
reg_kb_3.add(b_3)
reg_kb_4 = InlineKeyboardMarkup()
reg_kb_4.add(b_4)
reg_kb_5 = InlineKeyboardMarkup()
reg_kb_5.add(b_5)

b_1 = InlineKeyboardButton('ОТМЕНИТЬ РЕГИСТРАЦИЮ', callback_data='11')
b_2 = InlineKeyboardButton('ОТМЕНИТЬ РЕГИСТРАЦИЮ', callback_data='22')
b_3 = InlineKeyboardButton('ОТМЕНИТЬ РЕГИСТРАЦИЮ', callback_data='33')
b_4 = InlineKeyboardButton('ОТМЕНИТЬ РЕГИСТРАЦИЮ', callback_data='44')
b_5 = InlineKeyboardButton('ОТМЕНИТЬ РЕГИСТРАЦИЮ', callback_data='55')
reg_cancel_kb_1 = InlineKeyboardMarkup()
reg_cancel_kb_1.add(b_1)
reg_cancel_kb_2 = InlineKeyboardMarkup()
reg_cancel_kb_2.add(b_2)
reg_cancel_kb_3 = InlineKeyboardMarkup()
reg_cancel_kb_3.add(b_3)
reg_cancel_kb_4 = InlineKeyboardMarkup()
reg_cancel_kb_4.add(b_4)
reg_cancel_kb_5 = InlineKeyboardMarkup()
reg_cancel_kb_5.add(b_5)



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
