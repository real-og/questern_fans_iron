from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards as kb
import texts
from loader import dp, db
from states import State
from datetime import datetime
from aiogram.types import InputFile, InputMediaDocument

from checker import check_event_id

import fan_id_interface



@dp.message_handler(commands=["start"], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(texts.hello)

    media_terms = [
            InputMediaDocument(
                media=InputFile("files/01_Согласие_на_обработку_персональных_данных.pdf"),
            ),
            InputMediaDocument(
                media=InputFile("files/02_Согласие_на_информационные_и_рекламные_сообщения.pdf")
            )
        ]

    await message.answer_media_group(media_terms)
    await message.answer(texts.confirm, reply_markup=kb.get_agree_kb())
    await State.confirmation.set()
    start_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    await state.update_data(start_date=start_date)

    user = await db.get(message.from_user.id)
    
    if not user:
        all_users = await db.get_all()
        fan_id = fan_id_interface.get_fan_id(all_users)
        await db.add({"telegram_id": message.from_user.id, "start_date": start_date, "fan_id": fan_id})
    event_id = await check_event_id(message.from_user.id,"NN_event_id")


@dp.callback_query_handler(state=State.confirmation)
async def accept_documents(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.answer("Спасибо 👍")
    await callback.message.edit_text("Вы согласились с документами ✅")
    await state.update_data(confirm_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    await callback.message.answer(texts.menu, reply_markup=kb.menu_kb)
    await State.menu.set()
    await db.update(callback.from_user.id, confirm_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))




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


