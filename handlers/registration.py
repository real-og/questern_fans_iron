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
from datetime import datetime

import buttons

import side_logic

def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False


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
    text = "Напишите дату рождения в формате ДД.ММ.ГГГГ"
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await State.entering_birth.set()


@dp.message_handler(state=State.entering_birth)
async def handle_contact(message: types.Message, state: FSMContext):
    date = message.text
    if is_valid_date(date):
        await state.update_data(birth=date)
        text = 'Напишите в каком городе вы живете?'
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        await State.entering_city.set()
        
    else:
        text = "Не удалось распознать дату. Напишите ее в формате ДД.ММ.ГГГГ"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=State.entering_city)
async def handle_contact(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)

    data = await state.get_data()
    if data.get('email'):
        await message.answer('Спасибо! Данные сохранены!', reply_markup=kb.menu_kb)
        await State.menu.set()

    else:
        await message.answer(texts.enter_email, reply_markup=ReplyKeyboardRemove())
        await State.entering_email.set()


@dp.message_handler(state=State.entering_email)
async def send_welcome(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)

    fan_id = fan_id_interface.get_fan_id()
    await state.update_data(fan_number=fan_id)

    await message.answer(texts.register_success(int(fan_id)), reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()
    user_actions = data.get('user_actions_minsk')

    if user_actions:
        last_action = user_actions[-1]
        user_input = last_action

        data = await state.get_data()
        event_number = data.get('event_number')

        if not event_number:
            event_number = fan_id_interface.get_event_number()
            await state.update_data(event_number=event_number)
            await state.update_data(tumen_reg=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        user_actions = data.get('user_actions_tumen', [])
        user_actions.append(user_input)
        await state.update_data(user_actions_minsk=user_actions)

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


        elif user_input == buttons.guide:
            await message.answer(texts.guide_1, disable_web_page_preview=True)
            media = [
                types.InputMediaPhoto(types.InputFile("files/guide_1.jpg"), caption=texts.guide_2),
                types.InputMediaPhoto(types.InputFile("files/guide_2.jpg")),
                types.InputMediaPhoto(types.InputFile("files/guide_3.jpg")),
                types.InputMediaPhoto(types.InputFile("files/guide_4.jpg")),
                types.InputMediaPhoto(types.InputFile("files/guide_5.jpg")),
                types.InputMediaPhoto(types.InputFile("files/guide_6.jpg")),
            ]
            await message.answer_media_group(media)
            await message.answer(texts.guide_3, disable_web_page_preview=True)
            await message.answer(texts.guide_4, disable_web_page_preview=True)


        elif user_input == buttons.sales:
            file_id = 'BQACAgIAAxkDAAIWhmpF7YG9N_X6WW7pmz9Lj2jNYInXAAKDpwACHCYoSoxDzrTbhrBCPAQ'
            await message.answer_document(document=file_id, caption=texts.sales)
            # m = await message.answer_document(document=types.InputFile("files/Скидки_для_участников_и_болельщиков.pdf"), caption=texts.sales)
            # print(m)

        elif user_input == buttons.maps:
            # media = [
            #     types.InputMediaPhoto(types.InputFile("files/map_minsk_1.jpg"), caption='SWIMSTAR'),
            #     types.InputMediaPhoto(types.InputFile("files/map_minsk_2.jpg")),
            # ]
            # await message.answer_media_group(media)
            await message.answer_photo(photo=types.InputFile("files/map_tumen_1.jpg"), caption='IRONSTAR 113')
            await message.answer_photo(photo=types.InputFile("files/map_tumen_2.jpg"), caption='IRONSTAR ОЛИМПИК')
            await message.answer_photo(photo=types.InputFile("files/map_tumen_3.jpg"), caption='IRONLADY')
            await message.answer_photo(photo=types.InputFile("files/map_tumen_4.jpg"), caption='MANSTAR')
            await message.answer_photo(photo=types.InputFile("files/map_tumen_5.jpg"), caption='STARKIDS')
            await message.answer_photo(photo=types.InputFile("files/map_tumen_6.jpg"), caption='ЭКСПО')

        elif user_input == buttons.activity:
            await message.answer(texts.activity_0)
            await message.answer(texts.activity_1, reply_markup=kb.reg_kb_1)
            await message.answer(texts.activity_2, reply_markup=kb.reg_kb_2)
            await message.answer(texts.activity_3, reply_markup=kb.reg_kb_3)
            await message.answer(texts.activity_4, reply_markup=kb.reg_kb_4)
            await message.answer(texts.activity_5, reply_markup=kb.reg_kb_5)


        elif user_input == buttons.infocatalog:
            await message.answer(texts.infocatalog, disable_web_page_preview=True)


        elif user_input == buttons.schema:
            await message.answer_photo(photo=types.InputFile("files/schema_tumen.jpg"), caption=texts.schema)


        elif user_input == buttons.my_number:
            data = await state.get_data()
            fan_number = data.get('fan_number')
            event_number = data.get('event_number')
            registered_activities = data.get('registered_activities', [])
            await message.answer(texts.get_my_numbers(fan_number, event_number, registered_activities))

        
    await message.answer(texts.menu, reply_markup=kb.menu_kb)
    await State.menu.set()





