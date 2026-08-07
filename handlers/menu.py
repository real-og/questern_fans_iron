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
import fan_id_interface
from datetime import datetime

@dp.message_handler(state=State.menu)
async def send_welcome(message: types.Message, state: FSMContext):
    user_input = message.text
    data = await state.get_data()
    event_number = data.get('event_number')
    if not event_number:
        event_number = fan_id_interface.get_event_number()
        await state.update_data(event_number=event_number)
        await state.update_data(night_reg=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    user_actions = data.get('user_actions_night', [])
    user_actions.append(user_input)
    await state.update_data(user_actions_night=user_actions)

    if not data.get('name'):
        await message.answer(texts.enter_name, reply_markup=ReplyKeyboardRemove())
        await State.entering_name.set()
        return
    
    if not data.get('number'):
        await message.answer(texts.enter_number, reply_markup=kb.get_contact_kb())
        await State.entering_number.set()
        return
    

    if user_input == buttons.scheadule:
        await message.answer(texts.scheadule_1, disable_web_page_preview=True)
        await message.answer(texts.scheadule_2, disable_web_page_preview=True)
        await message.answer(texts.scheadule_3, disable_web_page_preview=True)
        await message.answer(texts.scheadule_4, disable_web_page_preview=True)

    elif user_input == buttons.guide:
        await message.answer(texts.guide_1, disable_web_page_preview=True)
        # media = [
        #     types.InputMediaPhoto(types.InputFile("files/guide_1.jpg"), caption=texts.guide_2),
        #     types.InputMediaPhoto(types.InputFile("files/guide_2.jpg")),
        #     types.InputMediaPhoto(types.InputFile("files/guide_3.jpg")),
        #     types.InputMediaPhoto(types.InputFile("files/guide_4.jpg")),
        #     types.InputMediaPhoto(types.InputFile("files/guide_5.jpg")),
        #     types.InputMediaPhoto(types.InputFile("files/guide_6.jpg")),
        # ]
        # await message.answer_media_group(media)
        # await message.answer(texts.guide_3, disable_web_page_preview=True)
        # await message.answer(texts.guide_4, disable_web_page_preview=True)



    elif user_input == buttons.sales:
        # await message.answer(texts.sales, disable_web_page_preview=True)
        file_id = 'BQACAgIAAxkDAAJlVGp1dzEQp7QVaxdidgOTzh0H0JA-AALkrQAC24WpS92Lc17MJ-YWPQQ'
        await message.answer_document(document=file_id, caption=texts.sales)
        # m = await message.answer_document(document=types.InputFile("files/Предложения_участникам_и_болельщикам.pdf"), caption=texts.sales)
        # print(m)

    elif user_input == buttons.maps:
        # media = [
        #     types.InputMediaPhoto(types.InputFile("files/map_minsk_1.jpg"), caption='SWIMSTAR'),
        #     types.InputMediaPhoto(types.InputFile("files/map_minsk_2.jpg")),
        # ]
        # await message.answer_media_group(media)
        await message.answer_photo(photo=types.InputFile("files/msk1.jpg"), caption='ЛИГА ТРИАТЛОНА & IRONSTAR МОСКВА 2026')
        await message.answer_photo(photo=types.InputFile("files/msk2.jpg"), caption='ЛИГА ТРИАТЛОНА & IRONSTAR МОСКВА 113')
        await message.answer_photo(photo=types.InputFile("files/msk3.jpg"), caption='STARKIDS')
        await message.answer_photo(photo=types.InputFile("files/msk4.jpg"), caption='ДЕТСКИЙ КУБОК ФТР 4-6 ЛЕТ')
        await message.answer_photo(photo=types.InputFile("files/msk5.jpg"), caption='ДЕТСКИЙ КУБОК ФТР 7-8 ЛЕТ')
        await message.answer_photo(photo=types.InputFile("files/msk6.jpg"), caption='ДЕТСКИЙ КУБОК ФТР 9-10 ЛЕТ')
        await message.answer_photo(photo=types.InputFile("files/msk7.jpg"), caption='ДЕТСКИЙ КУБОК ФТР 11-12 ЛЕТ')
        await message.answer_photo(photo=types.InputFile("files/msk8.jpg"), caption='ДЕТСКИЙ КУБОК ФТР 13-14 ЛЕТ')
        await message.answer_photo(photo=types.InputFile("files/msk9.jpg"), caption='СЕМЕЙНАЯ ЭСТАФЕТА')
        await message.answer_photo(photo=types.InputFile("files/msk10.jpg"), caption='СУПЕРСПРИНТ ТРОЙКА (ОТБОРОЧНЫЙ ТУР)')
        await message.answer_photo(photo=types.InputFile("files/msk11.jpg"), caption='СУПЕРСПРИНТ ТРОЙКА (ФИНАЛ)')
    # elif user_input == buttons.docs:
    #      m = await message.answer_document(document=types.InputFile("files/Согласие_с_условиями_участия_в_Ночном_забеге.docx"), caption=texts.docs, reply_markup=kb.menu_kb)


    elif user_input == buttons.activity:
        await message.answer(texts.activity_1)
        # await message.answer(texts.activity_1, reply_markup=kb.reg_kb_1)
        # await message.answer(texts.activity_2, reply_markup=kb.reg_kb_2)
        # await message.answer(texts.activity_3, reply_markup=kb.reg_kb_3)
        # await message.answer(texts.activity_4, reply_markup=kb.reg_kb_4)
        # await message.answer(texts.activity_5, reply_markup=kb.reg_kb_5)

    elif user_input == buttons.infocatalog:
        await message.answer(texts.infocatalog, disable_web_page_preview=True)

    # elif user_input == buttons.schema:
    #     await message.answer_photo(photo=types.InputFile("files/schema_tumen.jpg"), caption=texts.schema)

    elif user_input == buttons.my_number:
        data = await state.get_data()
        fan_number = data.get('fan_number')
        event_number = data.get('event_number')
        registered_activities = data.get('registered_activities_night', [])
        await message.answer(texts.get_my_numbers(fan_number, event_number, registered_activities))

    
    await message.answer(texts.menu, reply_markup=kb.menu_kb)

    