from aiogram import types
from aiogram.dispatcher import FSMContext

import db
import texts
from loader import dp


@dp.message_handler(commands=["start"], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer("1")

    sections = await db.get_visible_bot_sections()

    print("SECTIONS:", sections, flush=True)

    await message.answer(f"{message.from_user.language_code} - {texts.your_lang}")