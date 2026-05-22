from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards as kb
import db
import texts
from loader import dp
from states import State

import side_logic
from aiogram.types import ReplyKeyboardRemove
import buttons


@dp.message_handler(state=State.menu)
async def send_welcome(message: types.Message, state: FSMContext):
    user_input = message.text
    data = await state.get_data()
    user_actions = data.get('user_actions', [])
    user_actions.append(user_input)
    await state.update_data(user_actions=user_actions)

    if not data.get('name'):
        await message.answer(texts.enter_name, reply_markup=ReplyKeyboardRemove())
        await State.entering_name.set()
        return
    
    if not data.get('number'):
        await message.answer(texts.enter_number, reply_markup=kb.get_contact_kb())
        await State.entering_number.set()
        return
    


    if user_input == buttons.scheadule:
        await message.answer(texts.scheadule, disable_web_page_preview=True)

    elif user_input == buttons.points:
        await message.answer_photo(photo=types.InputFile("files/points.jpg"))
        await message.answer(texts.points, disable_web_page_preview=True)

    elif user_input == buttons.sales:
        await message.answer(texts.sales, disable_web_page_preview=True)

    elif user_input == buttons.schema:
        await message.answer(texts.schema)
        media = [
            types.InputMediaPhoto(types.InputFile("files/schema1.jpg")),
            types.InputMediaPhoto(types.InputFile("files/schema2.jpg")),
        ]
        await message.answer_media_group(media)

    elif user_input == buttons.politics:
        await message.answer('terms')
    
    await message.answer(texts.menu, reply_markup=kb.menu_kb)

    
    


