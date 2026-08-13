from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards as kb
import texts
from loader import dp
from states import State
from datetime import datetime

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile, InputMediaDocument
from loader import dp, bot


@dp.message_handler(commands=["start"], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(texts.hello)
    media = [
            InputMediaDocument(
                media=InputFile("files/01_Согласие_на_обработку_персональных_данных.pdf"),
            ),
            InputMediaDocument(
                media=InputFile("files/02_Согласие_на_информационные_и_рекламные_сообщения.pdf")
            )
        ]

    await message.answer_media_group(media)
    await message.answer(texts.confirm, reply_markup=kb.get_agree_kb())
    await State.confirmation.set()
    await state.update_data(start_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

@dp.callback_query_handler(state=State.confirmation)
async def accept_documents(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Спасибо 👍")
    await callback.message.edit_text("Вы согласились с документами ✅")
    await state.update_data(confirm_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    await callback.message.answer(texts.menu, reply_markup=kb.menu_kb)
    await State.menu.set()



@dp.message_handler(commands=["help"], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(texts.help)


@dp.message_handler(commands=["terms"], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    media = [
            InputMediaDocument(
                media=InputFile("files/01_Согласие_на_обработку_персональных_данных.pdf"),
            ),
            InputMediaDocument(
                media=InputFile("files/02_Согласие_на_информационные_и_рекламные_сообщения.pdf")
            )
        ]

    await message.answer_media_group(media)


