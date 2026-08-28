# import csv
# import json
# import os
# from datetime import datetime

# import redis
# from aiogram import types
# from aiogram.dispatcher import FSMContext

# from loader import dp, db


# REDIS_HOST = "127.0.0.1"
# REDIS_PORT = 6379
# REDIS_DB = 1
# REDIS_PASSWORD = None

# FSM_PREFIX = "fsm"


# redis_client = redis.Redis(
#     host=REDIS_HOST,
#     port=REDIS_PORT,
#     db=REDIS_DB,
#     password=REDIS_PASSWORD,
#     decode_responses=True,
# )


# def normalize_activities(value):
#     if not value:
#         return []

#     if isinstance(value, str):
#         value = [value]

#     if not isinstance(value, list):
#         return []

#     result = []

#     for item in value:
#         item = str(item or "").strip()

#         if item and item not in result:
#             result.append(item)

#     return result


# def get_nn_activities_from_redis():
#     """
#     Возвращает:
#     {
#         telegram_id: ["Активность 1", "Активность 2"],
#         ...
#     }
#     """

#     result = {}

#     pattern = f"{FSM_PREFIX}:*:*:data"

#     for key in redis_client.scan_iter(pattern):
#         # fsm:<chat_id>:<user_id>:data
#         parts = key.split(":")

#         if len(parts) < 4:
#             continue

#         user_id = str(parts[-2])

#         try:
#             data = json.loads(redis_client.get(key) or "{}")
#         except (json.JSONDecodeError, TypeError):
#             continue

#         activities = normalize_activities(
#             data.get("registered_activities_nn")
#         )

#         if activities:
#             result[user_id] = activities

#     return result


# def generate_activity_status_csv(
#     all_users,
#     registered_users,
#     filename
# ):
#     # telegram_id -> строка из table.csv
#     users_by_id = {
#         str(user.get("telegram_id")): user
#         for user in all_users
#     }

#     rows = []

#     for telegram_id, activities in registered_users.items():

#         user = users_by_id.get(str(telegram_id))

#         # В Redis пользователь есть, а в table.csv нет
#         if not user:
#             continue

#         for activity in activities:
#             rows.append({
#                 "Активность": activity,
#                 "Имя": user.get("name", ""),
#                 "Telegram ID": telegram_id,
#                 "Дата рождения": user.get("birth", ""),
#                 "Город": user.get("city", ""),
#                 "Email": user.get("email", ""),
#                 "Телефон": user.get("number", ""),
#             })

#     rows.sort(
#         key=lambda row: (
#             str(row["Активность"]).lower(),
#             str(row["Имя"]).lower(),
#             str(row["Telegram ID"]),
#         )
#     )

#     fieldnames = [
#         "Активность",
#         "Имя",
#         "Telegram ID",
#         "Дата рождения",
#         "Город",
#         "Email",
#         "Телефон",
#     ]

#     with open(
#         filename,
#         "w",
#         encoding="utf-8-sig",
#         newline=""
#     ) as f:

#         writer = csv.DictWriter(
#             f,
#             fieldnames=fieldnames,
#             delimiter=";",
#         )

#         writer.writeheader()
#         writer.writerows(rows)

#     return len(rows)


# @dp.message_handler(
#     commands=["activity_status"],
#     state="*"
# )
# async def activity_status_handler(
#     message: types.Message,
#     state: FSMContext
# ):
#     await message.answer(
#         "Формирую CSV по регистрациям на активности..."
#     )

#     filename = (
#         f"activity_status_"
#         f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
#     )

#     try:
#         # Основная база пользователей
#         all_users = await db.get_all()

#         # Из Redis берём ТОЛЬКО регистрации на активности
#         registered_users = get_nn_activities_from_redis()

#         rows_count = generate_activity_status_csv(
#             all_users=all_users,
#             registered_users=registered_users,
#             filename=filename,
#         )

#         if rows_count == 0:
#             await message.answer(
#                 "Регистраций на активности пока не найдено."
#             )
#             return

#         await message.answer_document(
#             document=types.InputFile(filename),
#             caption=f"Готово. Регистраций найдено: {rows_count}",
#         )

#     except Exception as e:
#         await message.answer(
#             f"Ошибка при формировании отчета: {e}"
#         )

#     finally:
#         if os.path.exists(filename):
#             os.remove(filename)