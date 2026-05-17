from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards as kb
import db
import texts
from loader import dp
from states import State

import side_logic


@dp.callback_query_handler(state=State.menu)
async def send_welcome(callback: types.CallbackQuery, state: FSMContext):
    button_id = callback.data
    await state.update_data(last_selected_button=button_id)
    data = await state.get_data()

    if not data.get('name'):
        await callback.message.answer(texts.enter_name)
        await State.entering_name.set()
        return
    
    if not data.get('surname'):
        callback.message.answer(texts.enter_surname)
        await State.entering_surname.set()
        return
    
    if not data.get('number'):
        await callback.message.answer(texts.enter_number, kb.get_contact_kb())
        await State.entering_number.set()
        return
    
    section = await db.get_bot_section(button_id)
    file_name = side_logic.get_file_if_exists('files', section.file_name)

    if section.content_text and file_name:
        await callback.message.answer_document(
            document=types.InputFile(file_name),
            caption=section.content_text
        )
    elif file_name:
        await callback.message.answer_document(
            document=types.InputFile(file_name)
        )

    elif section.content_text:
        await callback.message.answer(section.content_text)

    else:
        await callback.message.answer(texts.no_info)

    sections = await db.get_visible_bot_sections()
    await callback.message.answer(texts.menu, reply_markup=kb.get_bot_sections_kb(sections))
    await State.menu.set()
    await db.add_user_action(data.get('user_db_id'), button_id)


