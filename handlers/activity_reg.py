from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards as kb
import texts
from loader import dp, db
from states import State

from aiogram.types import ReplyKeyboardRemove
import buttons
import fan_id_interface
from datetime import datetime
from checker import check_event_id
from content import get_sirius_activities_from_redis


ACTIVITY_LIMITS = {
    '1': 50,
    '2': None,
    '3': 60,
    '4': 20,
    '5': None,
}

@dp.callback_query_handler(state=State.menu)
async def inline_button_handler(callback: types.CallbackQuery, state: FSMContext):
    event_id = await check_event_id(callback.from_user.id,"Sirius_event_id")

    if callback.data == '1':
        activity_name = 'КОФЕРАЙД С ИЛЬЕЙ И ЮЛИЕЙ ПРАСОЛОВЫМИ'
        await state.update_data(activity_1=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif callback.data == '2':
        activity_name = 'ФОТО-ПРОБЕЖКА ПО ОЛИМПИЙСКИМ ОБЪЕКТАМ'
        await state.update_data(activity_2=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif callback.data == '3':
        activity_name = 'ПРОБЕЖКА И ЗАВТРАК С ИЛЬЕЙ СЛЕПОВЫМ'
        await state.update_data(activity_3=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif callback.data == '4':
        activity_name = 'ТРЕНИРОВКА ПО ПЛАВАНИЮ С АНДРЕЕМ И АЛЕКСАНДРОМ БРЮХАНКОВЫМИ'
        await state.update_data(activity_4=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif callback.data == '5':
        activity_name = 'МАСТЕР-КЛАСС ПО ПРОХОЖДЕНИЮ ТРАНЗИТНОЙ ЗОНЫ'
        await state.update_data(activity_5=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    data = await state.get_data()
    user = await db.get(callback.from_user.id)
    registered_activities = data.get('registered_activities_sirius', [])

    if activity_name in registered_activities:
        await callback.message.answer("Вы уже зарегистрированы на эту активность", reply_markup=kb.menu_kb)
        return
    

    limit = ACTIVITY_LIMITS.get(callback.data)

    if limit is not None:
        registered_users = get_sirius_activities_from_redis()

        registered_count = sum(
            1
            for activities in registered_users.values()
            if activity_name in activities
        )

        if registered_count > limit:
            await callback.message.answer(
                "К сожалению, места на эту активность закончились 😔",
                reply_markup=kb.menu_kb
            )
            return
    

    if user.get('birth') and user.get('city'):
        text = f"""Вы успешно зарегистрированы✅

Активность: {activity_name}"""
        await callback.message.answer(text, reply_markup=kb.menu_kb)
        registered_activities.append(activity_name)
        await state.update_data(registered_activities_sirius=registered_activities)

    else:
        await callback.message.answer("Для регистрации на активность нужно дополнить ваши данные. Это займет не больше минуты 👇")
        await callback.message.answer( "Напишите дату рождения в формате ДД.ММ.ГГГГ")
        await State.entering_birth.set()


@dp.message_handler(state="*")
async def fallback_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "Не понял команду.\n\nНажмите /start"
    )
