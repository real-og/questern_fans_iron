from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards as kb
import db
import texts
from loader import dp
from states import State


@dp.message_handler(commands=["start"], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    sections = await db.get_visible_bot_sections()
    await message.answer(texts.hello, reply_markup=kb.get_bot_sections_kb(sections))
    await State.menu.set()


@dp.message_handler(commands=["help"], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(texts.help)


