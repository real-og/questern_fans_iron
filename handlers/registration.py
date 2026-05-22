from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

import keyboards as kb
import db
import texts
from loader import dp
from states import State
from aiogram import types
import fan_id_interface

import side_logic


@dp.message_handler(state=State.entering_name)
async def send_welcome(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(texts.enter_number, reply_markup=kb.get_contact_kb())
    await State.entering_number.set()


@dp.message_handler(state=State.entering_number, content_types=types.ContentTypes.ANY)
async def handle_contact(message: types.Message, state: FSMContext):
    if not message.contact:
        await message.answer(texts.enter_number, reply_markup=kb.get_contact_kb())
        return

    number = message.contact.phone_number
    await state.update_data(number=number)

    fan_id = fan_id_interface.get_fan_id()
    await state.update_data(fan_id=fan_id)
    await message.answer(texts.register_success(int(fan_id)), reply_markup=ReplyKeyboardRemove())
    await message.answer(texts.menu, reply_markup=kb.menu_kb)
    await State.menu.set()





