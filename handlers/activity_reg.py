# from aiogram import types
# from aiogram.dispatcher import FSMContext

# import keyboards as kb
# import texts
# from loader import dp, db
# from states import State

# from aiogram.types import ReplyKeyboardRemove
# import buttons
# import fan_id_interface
# from datetime import datetime
# from checker import check_event_id

# @dp.callback_query_handler(state=State.menu)
# async def inline_button_handler(callback: types.CallbackQuery, state: FSMContext):
#     event_id = await check_event_id(callback.from_user.id,"NN_event_id")

#     if callback.data == '1':
#         activity_name = 'SUNSET RUN'
#         await state.update_data(activity_1=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#     elif callback.data == '2':
#         activity_name = 'Т1 и Т2: исправляем Т9'
#         await state.update_data(activity_2=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#     # elif callback.data == '3':
#     #     activity_name = 'Фото-пробежка с Данилой Курниковым'
#     #     await state.update_data(activity_3=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#     # elif callback.data == '4':
#     #     activity_name = 'Мастер-класс по прохождению транзитной зоны Т1 от Марии Шейкиной и сети магазинов «Велоспорт»'
#     #     await state.update_data(activity_4=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#     # elif callback.data == '5':
#     #     activity_name = 'Вечеринка финишеров'
#     #     await state.update_data(activity_5=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

#     data = await state.get_data()
#     user = await db.get(callback.from_user.id)
#     registered_activities = data.get('registered_activities_nn', [])

#     if activity_name in registered_activities:
#         await callback.message.answer("Вы уже зарегистрированы на эту активность", reply_markup=kb.menu_kb)
#         return
    

#     if user.get('birth') and user.get('city'):
#         text = f"""Вы успешно зарегистрированы✅

# Активность: {activity_name}"""
#         await callback.message.answer(text, reply_markup=kb.menu_kb)
#         registered_activities.append(activity_name)
#         await state.update_data(registered_activities_nn=registered_activities)

#     else:
#         await callback.message.answer("Для регистрации на активность нужно дополнить ваши данные. Это займет не больше минуты 👇")
#         await callback.message.answer( "Напишите дату рождения в формате ДД.ММ.ГГГГ")
#         await State.entering_birth.set()


# @dp.message_handler(state="*")
# async def fallback_handler(message: types.Message, state: FSMContext):
#     await message.answer(
#         "Не понял команду.\n\nНажмите /start"
#     )
