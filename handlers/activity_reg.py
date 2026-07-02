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

@dp.callback_query_handler(state=State.menu)
async def inline_button_handler(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == '1':
        activity_name = 'Городской интерактивный квест IRONSTAR'
        await state.update_data(activity_1=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif callback.data == '2':
        activity_name = 'Йога и медитация с поющими чашами от LIME FITNESS'
        await state.update_data(activity_2=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif callback.data == '3':
        activity_name = 'Фото-пробежка с Данилой Курниковым'
        await state.update_data(activity_3=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif callback.data == '4':
        activity_name = 'Мастер-класс по прохождению транзитной зоны Т1 от Марии Шейкиной и сети магазинов «Велоспорт»'
        await state.update_data(activity_4=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif callback.data == '5':
        activity_name = 'Вечеринка финишеров'
        await state.update_data(activity_5=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    data = await state.get_data()
    registered_activities = data.get('registered_activities', [])

    if activity_name in registered_activities:
        await callback.message.answer("Вы уже зарегистрированы на эту активность", reply_markup=kb.menu_kb)
        return
    

        

    if data.get('birth') and data.get('city'):
        text = f"""Вы успешно зарегистрированы✅

Активность: {activity_name}"""
        await callback.message.answer(text, reply_markup=kb.menu_kb)
        registered_activities.append(activity_name)
        await state.update_data(registered_activities=registered_activities)

    else:
        await callback.message.answer("Для регистрации на активность нужно дополнить ваши данные. Это займет не больше минуты 👇")
        await callback.message.answer( "Напишите дату рождения в формате ДД.ММ.ГГГГ")
        await State.entering_birth.set()
