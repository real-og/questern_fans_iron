from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

import keyboards as kb
import texts
from loader import dp, db
from states import State
from aiogram import types
import fan_id_interface
from datetime import datetime
import re

import buttons
from checker import check_event_id


def is_email(string):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(pattern, string) is not None

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
    await db.update(message.from_user.id, name=name)
    await State.entering_number.set()


@dp.message_handler(state=State.entering_number, content_types=types.ContentTypes.ANY)
async def handle_contact(message: types.Message, state: FSMContext):
    if not message.contact:
        await message.answer(texts.enter_number, reply_markup=kb.get_contact_kb())
        return

    number = message.contact.phone_number
    await state.update_data(number=number)
    await db.update(message.from_user.id, number=number)
    text = "Напишите дату рождения в формате ДД.ММ.ГГГГ"
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await State.entering_birth.set()


@dp.message_handler(state=State.entering_birth)
async def handle_contact(message: types.Message, state: FSMContext):
    date = message.text
    if is_valid_date(date):
        await state.update_data(birth=date)
        await db.update(message.from_user.id, birth=date)
        text = 'Напишите в каком городе вы живете?'
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        await State.entering_city.set()
        
    else:
        text = "Не удалось распознать дату. Напишите ее в формате ДД.ММ.ГГГГ"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=State.entering_city)
async def handle_contact(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await db.update(message.from_user.id, city=message.text)
    user = await db.get(message.from_user.id)

    data = await state.get_data()
    if user.get('email'):
        await message.answer('Спасибо! Данные сохранены!', reply_markup=kb.menu_kb)
        await State.menu.set()

    else:
        await message.answer(texts.enter_email, reply_markup=ReplyKeyboardRemove())
        await State.entering_email.set()


@dp.message_handler(state=State.entering_email)
async def send_welcome(message: types.Message, state: FSMContext):
    event_id = await check_event_id(message.from_user.id,"NN_event_id")
    email = message.text
    
    if not is_email(email):
        await message.answer('Неверный формат email, введите еще раз')
        return

    await state.update_data(email=email)
    await db.update(message.from_user.id, email=email)

    user = await db.get(message.from_user.id)


    await message.answer(texts.register_success(int(user.get('fan_id'))), reply_markup=ReplyKeyboardRemove())



    data = await state.get_data()
    if not data.get('nn_date'):
        await state.update_data(nn_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    user_actions = data.get('user_actions_nn')

    if user_actions:
        last_action = user_actions[-1]
        user_input = last_action

        data = await state.get_data()
        if not data.get('nn_date'):
            await state.update_data(nn_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


        user_actions = data.get('user_actions_nn', [])
        user_actions.append(user_input)
        await state.update_data(user_actions_nn=user_actions)

        user = await db.get(message.from_user.id)

        if not user.get('name'):
            await message.answer(texts.enter_name, reply_markup=ReplyKeyboardRemove())
            await State.entering_name.set()
            return
        
        if not user.get('number'):
            await message.answer(texts.enter_number, reply_markup=kb.get_contact_kb())
            await State.entering_number.set()
            return
        
        if user_input == buttons.scheadule:
            await message.answer(texts.scheadule_1, disable_web_page_preview=True)
            await message.answer(texts.scheadule_2, disable_web_page_preview=True)

        elif user_input == buttons.infocatalog:
            await message.answer_photo(photo=types.InputFile("files/info.jpg"), caption=texts.infocatalog, reply_markup=kb.menu_kb)



        elif user_input == buttons.guide:
            await message.answer(texts.guide_1, disable_web_page_preview=True)
            media = [
                types.InputMediaPhoto(types.InputFile("files/guide1.jpg")),
                types.InputMediaPhoto(types.InputFile("files/guide2.jpg")),
                types.InputMediaPhoto(types.InputFile("files/guide3.jpg")),
                types.InputMediaPhoto(types.InputFile("files/guide4.jpg")),
                types.InputMediaPhoto(types.InputFile("files/guide5.jpg")),
                types.InputMediaPhoto(types.InputFile("files/guide6.jpg")),
                types.InputMediaPhoto(types.InputFile("files/guide7.jpg")),
                types.InputMediaPhoto(types.InputFile("files/guide8.jpg")),
                types.InputMediaPhoto(types.InputFile("files/guide9.jpg")),
            ]
            await message.answer_media_group(media)
            await message.answer(texts.guide_2, disable_web_page_preview=True)
            await message.answer(texts.guide_3, disable_web_page_preview=True, reply_markup=kb.menu_kb)



        elif user_input == buttons.sales:
            # await message.answer(texts.sales, disable_web_page_preview=True)
            # file_id = 'BQACAgIAAxkDAAJlVGp1dzEQp7QVaxdidgOTzh0H0JA-AALkrQAC24WpS92Lc17MJ-YWPQQ'
            # await message.answer_document(document=file_id, caption=texts.sales)
            m = await message.answer_document(document=types.InputFile("files/Акции IRONSTAR НН.pdf"), caption=texts.sales)
            print(m)

        elif user_input == buttons.maps:
            await message.answer_photo(photo=types.InputFile("files/map1.jpg"), caption='<b>IRONSTAR 113</b>')
            await message.answer_photo(photo=types.InputFile("files/map2.jpg"), caption='<b>IRONSTAR ОЛИМПИЙСКАЯ</b>')
            await message.answer_photo(photo=types.InputFile("files/map3.jpg"), caption='<b>SWIMSTAR 1 МИЛЯ</b>')
            await message.answer_photo(photo=types.InputFile("files/map4.jpg"), caption='<b>SWIMSTAR 1K / 2K ЭСТАФЕТА</b>')
            await message.answer_photo(photo=types.InputFile("files/map5.jpg"), caption='<b>IRONLADY</b>')
            await message.answer_photo(photo=types.InputFile("files/map6.jpg"), caption='<b>MANSTAR</b>')
            await message.answer_photo(photo=types.InputFile("files/map7.jpg"), caption='<b>STARKIDS</b>')

        # elif user_input == buttons.docs:
        #      m = await message.answer_document(document=types.InputFile("files/Согласие_с_условиями_участия_в_Ночном_забеге.docx"), caption=texts.docs, reply_markup=kb.menu_kb)


        elif user_input == buttons.activity:
            await message.answer_photo(photo=types.InputFile("files/activity1.jpg"), caption=texts.activity_1, reply_markup=kb.reg_kb_1)
            await message.answer_photo(photo=types.InputFile("files/activity2.jpg"), caption=texts.activity_2, reply_markup=kb.reg_kb_2)
            # await message.answer(texts.activity_1)
            # await message.answer(texts.activity_1, reply_markup=kb.reg_kb_1)
            # await message.answer(texts.activity_2, reply_markup=kb.reg_kb_2)
            # await message.answer(texts.activity_3, reply_markup=kb.reg_kb_3)
            # await message.answer(texts.activity_4, reply_markup=kb.reg_kb_4)
            # await message.answer(texts.activity_5, reply_markup=kb.reg_kb_5)

        # elif user_input == buttons.infocatalog:
        #     await message.answer(texts.infocatalog, disable_web_page_preview=True)

        elif user_input == buttons.schema:
            media = [
                types.InputMediaPhoto(types.InputFile("files/schema1.jpg")),
                types.InputMediaPhoto(types.InputFile("files/schema2.jpg"))
            ]
            await message.answer_media_group(media)
            await message.answer(texts.schema, disable_web_page_preview=True)

        elif user_input == buttons.my_number:
            data = await state.get_data()

            fan_id = user.get('fan_id')
            event_id = user.get('NN_event_id')
            registered_activities = data.get('registered_activities_nn', [])
            await message.answer(texts.get_my_numbers(fan_id, event_id, registered_activities))

            
        
    await message.answer(texts.menu, reply_markup=kb.menu_kb)
    await State.menu.set()





