from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards as kb
import db
import texts
from loader import dp
from states import State
from datetime import datetime


@dp.message_handler(commands=["start"], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(texts.hello, reply_markup=kb.menu_kb)
    await State.menu.set()
    await state.update_data(start_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


@dp.message_handler(commands=["help"], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(texts.help)


@dp.message_handler(commands=["terms"], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer_document(document=types.InputFile("files/terms.pdf"), caption='Политика обработки персональных данных')


