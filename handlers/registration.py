from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards as kb
import db
import texts
from loader import dp
from states import State
from aiogram import types

import side_logic


@dp.message_handler(state=State.entering_name)
async def send_welcome(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(texts.enter_surname)
    await State.entering_surname.set()


@dp.message_handler(state=State.entering_surname)
async def send_welcome(message: types.Message, state: FSMContext):
    surname = message.text
    await state.update_data(surname=surname)
    await message.answer(texts.enter_number, reply_markup=kb.get_contact_kb())
    await State.entering_number.set()


@dp.message_handler(state=State.entering_number, content_types=types.ContentTypes.ANY)
async def handle_contact(message: types.Message, state: FSMContext):
    if not message.contact:
        await message.answer(texts.enter_number, reply_markup=kb.get_contact_kb())
        return

    number = message.contact.phone_number
    await state.update_data(number=number)
    data = await state.get_data()
    name = data.get('name')
    surname = data.get('surname')
    last_selected_button = data.get('last_selected_button')

    result_db = await db.upsert_user(telegram_id=message.from_user.id,
                                     first_name=name,
                                     last_name=surname,
                                     phone=number)
    await state.update_data(user_db_id=result_db.user_id)
    await message.answer(texts.register_success(int(result_db.user_id)))
    section = await db.get_bot_section(last_selected_button)

    file_name = side_logic.get_file_if_exists('files', section.file_name)


    if section.content_text and file_name:
        await message.answer_document(
            document=types.InputFile(file_name),
            caption=section.content_text
        )
    elif file_name:
        await message.answer_document(
            document=types.InputFile(file_name)
        )

    elif section.content_text:
        await message.answer(section.content_text)

    else:
        await message.answer(texts.no_info)
    
    await db.add_user_action(result_db.user_id, last_selected_button)

    sections = await db.get_visible_bot_sections()
    await message.answer(texts.menu, reply_markup=kb.get_bot_sections_kb(sections))
    await State.menu.set()





