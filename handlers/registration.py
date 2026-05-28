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

import buttons

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

    data = await state.get_data()
    user_actions = data.get('user_actions_voronez')

    if user_actions:
        last_action = user_actions[-1]
        user_input = last_action

        if user_input == buttons.scheadule:
            await message.answer(texts.scheadule_1, disable_web_page_preview=True)
            await message.answer(texts.scheadule_2, disable_web_page_preview=True)
            await message.answer(texts.scheadule_3, disable_web_page_preview=True)

        elif user_input == buttons.guide:
            await message.answer(texts.guide_1)
            await message.answer(texts.guide_2)
            await message.answer(texts.guide_3)
            await message.answer(texts.guide_4)

        elif user_input == buttons.sales:
            file_id = 'BQACAgEAAxkDAAIB02oYiH2jBoJrrIbqnGtUOKNaLqAqAAJSBwACELHBRGtQIO0gwfvQOwQ'
            await message.answer_document(document=file_id, caption=texts.sales)
            # m = await message.answer_document(document=types.InputFile("files/sales_voronezh.pdf"), caption=texts.sales)
            # print(m)

        elif user_input == buttons.maps:
            await message.answer_photo(photo=types.InputFile("files/map_voronez_1.png"), caption='IRONSTAR 1/8')
            await message.answer_photo(photo=types.InputFile("files/map_voronez_2.png"), caption='IRONSTAR 1/4')
            await message.answer_photo(photo=types.InputFile("files/map_voronez_3.png"), caption='IRONLADY')
            await message.answer_photo(photo=types.InputFile("files/map_voronez_4.png"), caption='MANSTAR')
            await message.answer_photo(photo=types.InputFile("files/map_voronez_5.png"), caption='JUNIORSTAR')
            await message.answer_photo(photo=types.InputFile("files/map_voronez_6.png"), caption='STARKIDS')
            await message.answer_photo(photo=types.InputFile("files/map_voronez_7.png"), caption='ЭКСПО')

        elif user_input == buttons.activity:
            await message.answer(texts.activity)

        elif user_input == buttons.infocatalog:
            await message.answer(texts.infocatalog, disable_web_page_preview=True)

        elif user_input == buttons.schema:
            await message.answer(texts.schema)
            media = [
                types.InputMediaPhoto(types.InputFile("files/voronez_perecrit_1.jpg")),
                types.InputMediaPhoto(types.InputFile("files/voronez_perecrit_2.jpg")),
            ]
            await message.answer_media_group(media)
        
    await message.answer(texts.menu, reply_markup=kb.menu_kb)
    await State.menu.set()





