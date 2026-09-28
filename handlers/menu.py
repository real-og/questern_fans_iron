from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards as kb

import texts
from loader import dp, db
from states import State
from checker import check_event_id


from aiogram.types import ReplyKeyboardRemove
import buttons
import fan_id_interface
from datetime import datetime

@dp.message_handler(state=State.menu)
async def send_welcome(message: types.Message, state: FSMContext):
    event_id = await check_event_id(message.from_user.id,"Sirius_event_id")
    user_input = message.text
    data = await state.get_data()
    if not data.get('sirius_date'):
        await state.update_data(sirius_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    user_actions = data.get('user_actions_sirius', [])
    user_actions.append(user_input)
    await state.update_data(user_actions_sirius=user_actions)

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
        # file_id = 'BQACAgIAAxkDAALHoGqRRkIey4eDUsnMeuP2e9fFobk9AALeoAACoLmJSIFeFhrk6WXjPQQ'
        # await message.answer_document(document=file_id, caption=texts.scheadule_1)
        m = await message.answer_document(document=types.InputFile("files/Расписание_Сириус_2026.pdf"), caption=texts.scheadule_1)
        print(m)

    elif user_input == buttons.infocatalog:
        await message.answer(texts.infocatalog, disable_web_page_preview=True)



    # elif user_input == buttons.guide:
    #     await message.answer(texts.guide_1, disable_web_page_preview=True)
        # media = [
        #     types.InputMediaPhoto(types.InputFile("files/guide1.jpg")),
        #     types.InputMediaPhoto(types.InputFile("files/guide2.jpg")),
        #     types.InputMediaPhoto(types.InputFile("files/guide3.jpg")),
        #     types.InputMediaPhoto(types.InputFile("files/guide4.jpg")),
        #     types.InputMediaPhoto(types.InputFile("files/guide5.jpg")),
        #     types.InputMediaPhoto(types.InputFile("files/guide6.jpg")),
        #     types.InputMediaPhoto(types.InputFile("files/guide7.jpg")),
        #     types.InputMediaPhoto(types.InputFile("files/guide8.jpg")),
        #     types.InputMediaPhoto(types.InputFile("files/guide9.jpg")),
        # ]
        # await message.answer_media_group(media)
        # await message.answer(texts.guide_2, disable_web_page_preview=True)
        # await message.answer(texts.guide_3, disable_web_page_preview=True, reply_markup=kb.menu_kb)



    elif user_input == buttons.sales:
        # await message.answer(texts.sales, disable_web_page_preview=True)
        file_id = 'BQACAgIAAxkDAALQi2q3OdzSmHrl90a_t1GDRKWMTq4TAALZsAACi7q5SXpVltW6sC51PQQ'
        await message.answer_document(document=file_id, caption=texts.sales)
        # m = await message.answer_document(document=types.InputFile("files/Скидки_Сириус_2026.pdf"), caption=texts.sales)
        # print(m)

    elif user_input == buttons.maps:
        # await message.answer_photo(photo=types.InputFile("files/map1.png"), caption='IRONSTAR 1/4')
        # await message.answer_photo(photo=types.InputFile("files/map2.png"), caption='IRONSTAR 1/8')
        # media = [
        #     types.InputMediaPhoto(types.InputFile("files/map1.png"), caption='СУПЕРМИКС'),
        #     types.InputMediaPhoto(types.InputFile("files/map4.png"))
        # ]
        # await message.answer_media_group(media)
        # await message.answer_photo(photo=types.InputFile("files/map1.png"))
        # await message.answer_photo(photo=types.InputFile("files/map4.png"), caption='СУПЕРМИКС')
        await message.answer_photo(photo=types.InputFile("files/map1.jpg"), caption='113')
        await message.answer_photo(photo=types.InputFile("files/map2.jpg"), caption='Олимпийская дистанция')
        await message.answer_photo(photo=types.InputFile("files/map3.jpg"), caption='1/8')
        await message.answer_photo(photo=types.InputFile("files/map4.jpg"), caption='СУПЕРФИНАЛ')
        await message.answer_photo(photo=types.InputFile("files/map5.jpg"), caption='Всероссийское соревнование и Кубок IRONSTAR по паратриатлону')
        await message.answer_photo(photo=types.InputFile("files/map6.jpg"), caption='SWIMSTAR 1 и 2 мили')
        await message.answer_photo(photo=types.InputFile("files/map7.jpg"), caption='SWIMSTAR 1К и 2К ЭСТАФЕТА')
        await message.answer_photo(photo=types.InputFile("files/map8.jpg"), caption='MANSTAR')
        await message.answer_photo(photo=types.InputFile("files/map9.jpg"), caption='IRONLADY')
        await message.answer_photo(photo=types.InputFile("files/map10.jpg"), caption='STARKIDS')

    # elif user_input == buttons.docs:
    #      m = await message.answer_document(document=types.InputFile("files/Согласие_с_условиями_участия_в_Ночном_забеге.docx"), caption=texts.docs, reply_markup=kb.menu_kb)


    elif user_input == buttons.activity:
        # await message.answer_photo(photo=types.InputFile("files/activity1.jpg"), caption=texts.activity_1, reply_markup=kb.reg_kb_1)
        # await message.answer_photo(photo=types.InputFile("files/activity2.jpg"), caption=texts.activity_2, reply_markup=kb.reg_kb_2)
        # await message.answer(texts.activity_1)
        registered = data.get('registered_activities_sirius', [])
        if 'КОФЕРАЙД С ИЛЬЕЙ И ЮЛИЕЙ ПРАСОЛОВЫМИ' in registered:
            kb_1 = kb.reg_cancel_kb_1
        else:
            kb_1 = kb.reg_kb_1

        if 'ФОТО-ПРОБЕЖКА ПО ОЛИМПИЙСКИМ ОБЪЕКТАМ' in registered:
            kb_2 = kb.reg_cancel_kb_2
        else:
            kb_2 = kb.reg_kb_2

        if 'ПРОБЕЖКА И ЗАВТРАК С ИЛЬЕЙ СЛЕПОВЫМ' in registered:
            kb_3 = kb.reg_cancel_kb_3
        else:
            kb_3 = kb.reg_kb_3

        if 'ТРЕНИРОВКА ПО ПЛАВАНИЮ С АНДРЕЕМ И АЛЕКСАНДРОМ БРЮХАНКОВЫМИ' in registered:
            kb_4 = kb.reg_cancel_kb_4
        else:
            kb_4 = kb.reg_kb_4

        if 'МАСТЕР-КЛАСС ПО ПРОХОЖДЕНИЮ ТРАНЗИТНОЙ ЗОНЫ' in registered:
            kb_5 = kb.reg_cancel_kb_5
        else:
            kb_5 = kb.reg_kb_5
        await message.answer(texts.activity_1, reply_markup=kb_1, disable_web_page_preview=True)
        await message.answer(texts.activity_2, reply_markup=kb_2, disable_web_page_preview=True)
        await message.answer(texts.activity_3, reply_markup=kb_3, disable_web_page_preview=True)
        await message.answer(texts.activity_4, reply_markup=kb_4, disable_web_page_preview=True)
        await message.answer(texts.activity_5, reply_markup=kb_5, disable_web_page_preview=True)

    elif user_input == buttons.lectory:
        await message.answer(texts.lectory_0, disable_web_page_preview=True)
        await message.answer(texts.lectory_1, reply_markup=kb.kb_lectory_1, disable_web_page_preview=True)
        await message.answer(texts.lectory_2, reply_markup=kb.kb_lectory_2, disable_web_page_preview=True)
        await message.answer(texts.lectory_3, reply_markup=kb.kb_lectory_3, disable_web_page_preview=True)
        await message.answer(texts.lectory_4, reply_markup=kb.kb_lectory_4, disable_web_page_preview=True)
        await message.answer(texts.lectory_5, reply_markup=kb.kb_lectory_5, disable_web_page_preview=True)


    # elif user_input == buttons.infocatalog:
    #     await message.answer(texts.infocatalog, disable_web_page_preview=True)

    elif user_input == buttons.schema:
        await message.answer(texts.schema_1)
        # media = [
        #     types.InputMediaPhoto(types.InputFile("files/schema1.jpg"), caption=texts.schema_1),
        #     types.InputMediaPhoto(types.InputFile("files/schema2.jpg"))
        # ]
        # await message.answer_media_group(media)
        # await message.answer_photo(photo=types.InputFile("files/schema3.jpg"), caption=texts.schema_2)

    # elif user_input == buttons.transfer:
    #     await message.answer_photo(photo=types.InputFile("files/transfer.jpg"), caption=texts.transfer)
        

    elif user_input == buttons.my_number:
        data = await state.get_data()

        fan_id = user.get('fan_id')
        event_id = user.get('Sirius_event_id')
        registered_activities = data.get('registered_activities_sirius', [])
        registered_lectorys = data.get('registered_lectorys_sirius', [])
        await message.answer(texts.get_my_numbers(fan_id, event_id, registered_activities, registered_lectorys))

    
    await message.answer(texts.menu, reply_markup=kb.menu_kb)

    