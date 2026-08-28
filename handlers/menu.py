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
    event_id = await check_event_id(message.from_user.id,"Zavidovo_event_id")
    user_input = message.text
    data = await state.get_data()
    if not data.get('zavidovo_date'):
        await state.update_data(zavidovo_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    user_actions = data.get('user_actions_zavidovo', [])
    user_actions.append(user_input)
    await state.update_data(user_actions_zavidovo=user_actions)

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
        file_id = 'BQACAgIAAxkDAALHoGqRRkIey4eDUsnMeuP2e9fFobk9AALeoAACoLmJSIFeFhrk6WXjPQQ'
        await message.answer_document(document=file_id, caption=texts.scheadule_1)
        # m = await message.answer_document(document=types.InputFile("files/Расписание.pdf"), caption=texts.scheadule_1)
        # print(m)

    elif user_input == buttons.infocatalog:
        await message.answer_photo(photo=types.InputFile("files/info.jpg"), caption=texts.infocatalog)



    elif user_input == buttons.guide:
        await message.answer(texts.guide_1, disable_web_page_preview=True)
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
        file_id = 'BQACAgIAAxkDAALHzmqRSG8ab2a-rPG9GZu0GpjUQwtgAAJToQACoLmJSFH_VRgxQxEKPQQ'
        await message.answer_document(document=file_id, caption=texts.sales)
        # m = await message.answer_document(document=types.InputFile("files/скидки и предложения Завидово 2026.pdf"), caption=texts.sales)
        # print(m)

    elif user_input == buttons.maps:
        await message.answer_photo(photo=types.InputFile("files/map1.png"), caption='IRONSTAR 1/4')
        await message.answer_photo(photo=types.InputFile("files/map2.png"), caption='IRONSTAR 1/8')
        media = [
            types.InputMediaPhoto(types.InputFile("files/map1.jpg"), caption='СУПЕРМИКС'),
            types.InputMediaPhoto(types.InputFile("files/map4.jpg"))
        ]
        await message.answer_media_group(media)
        # await message.answer_photo(photo=types.InputFile("files/map1.png"))
        # await message.answer_photo(photo=types.InputFile("files/map4.png"), caption='СУПЕРМИКС')
        await message.answer_photo(photo=types.InputFile("files/map5.png"), caption='СВИМРАН')
        await message.answer_photo(photo=types.InputFile("files/map6.png"), caption='SWIMSTAR 1 МИЛЯ / 2 МИЛИ')
        await message.answer_photo(photo=types.InputFile("files/map7.png"), caption='SWIMSTAR 1K / 2K ЭСТАФЕТА')
        await message.answer_photo(photo=types.InputFile("files/map8.png"), caption='IRONLADY')
        await message.answer_photo(photo=types.InputFile("files/map9.png"), caption='MANSTAR')
        await message.answer_photo(photo=types.InputFile("files/map10.png"), caption='STARKIDS')

    # elif user_input == buttons.docs:
    #      m = await message.answer_document(document=types.InputFile("files/Согласие_с_условиями_участия_в_Ночном_забеге.docx"), caption=texts.docs, reply_markup=kb.menu_kb)


    # elif user_input == buttons.activity:
    #     await message.answer_photo(photo=types.InputFile("files/activity1.jpg"), caption=texts.activity_1, reply_markup=kb.reg_kb_1)
    #     await message.answer_photo(photo=types.InputFile("files/activity2.jpg"), caption=texts.activity_2, reply_markup=kb.reg_kb_2)
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
            types.InputMediaPhoto(types.InputFile("files/schema1.jpg"), caption=texts.schema_1),
            types.InputMediaPhoto(types.InputFile("files/schema2.jpg"))
        ]
        await message.answer_media_group(media)
        await message.answer_photo(photo=types.InputFile("files/schema3.jpg"), caption=texts.schema_2)

    elif user_input == buttons.transfer:
        await message.answer_photo(photo=types.InputFile("files/transfer.jpg"), caption=texts.transfer)
        

    elif user_input == buttons.my_number:
        data = await state.get_data()

        fan_id = user.get('fan_id')
        event_id = user.get('Zavidovo_event_id')
        registered_activities = data.get('registered_activities_zavidovo', [])
        await message.answer(texts.get_my_numbers(fan_id, event_id, registered_activities))

    
    await message.answer(texts.menu, reply_markup=kb.menu_kb)

    