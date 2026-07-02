from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts
from aiogram.types import InputFile
from states import State
import loader
import keyboards as kb
from aiogram.types import ReplyKeyboardRemove
import os

# CONTENT_DIR = 'files'

# def _chunk_text(text: str, limit: int = 3500):

#     parts = []
#     buf = []
#     size = 0
#     for line in text.splitlines(True):
#         if size + len(line) > limit and buf:
#             parts.append("".join(buf))
#             buf, size = [], 0
#         buf.append(line)
#         size += len(line)
#     if buf:
#         parts.append("".join(buf))
#     return parts


# @dp.message_handler(commands=['add'], state="*")
# async def send_welcome(message: types.Message, state: FSMContext):
#    await message.answer("Пришлите сюда файл, который положить на сервер. Чтобы выйти, используйте команду /start")
#    await State.adding.set()


# @dp.message_handler(state=State.adding)
# async def send_welcome(message: types.Message, state: FSMContext):
#     await message.answer("Пришлите сюда файл, который положить на сервер. Чтобы выйти, используйте команду /start")


# @dp.message_handler(state=State.adding, content_types=types.ContentType.DOCUMENT)
# async def handle_document(message: types.Message, state: FSMContext):
#     doc: types.Document = message.document
#     filename = doc.file_name or f"{doc.file_unique_id}"
#     save_path = os.path.join(CONTENT_DIR, filename)
#     await doc.download(destination_file=save_path)
#     await message.reply(f"✅ Сохранено: {save_path}")
#     await message.answer("Можете прислать еще файл для загрузки на сервер. Чтобы выйти, используйте команду /start")
    


# @dp.message_handler(commands=['items'], state="*")
# async def send_welcome(message: types.Message, state: FSMContext):
#     items = []
#     for name in sorted(os.listdir(CONTENT_DIR)):
#         path = os.path.join(CONTENT_DIR, name)
#         if os.path.isfile(path):
#             items.append(name)

#     if not items:
#         await message.reply("Файлы отсутствуют.")
#         return

#     text = "Файлы на сервере:\n" + "\n".join(f"• {x}" for x in items)
#     for part in _chunk_text(text):
#         await message.answer(part)



import csv
import json
import os
from datetime import datetime

import redis
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor


# =========================
# НАСТРОЙКИ
# =========================



REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_PASSWORD = None

FSM_PREFIX = "fsm" 



def to_int_if_possible(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return value


def parse_fsm_key(key: str, prefix: str):
    """
    Ожидаемый формат RedisStorage2:
    fsm:<chat_id>:<user_id>:state
    fsm:<chat_id>:<user_id>:data
    fsm:<chat_id>:<user_id>:bucket
    """

    prefix_part = prefix + ":"

    if not key.startswith(prefix_part):
        return None

    without_prefix = key[len(prefix_part):]

    try:
        chat_id, user_id, key_type = without_prefix.split(":", 2)
    except ValueError:
        return None

    return {
        "chat_id": to_int_if_possible(chat_id),
        "user_id": to_int_if_possible(user_id),
        "key_type": key_type,
    }


def get_all_bot_users():
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True,
    )

    users = {}

    patterns = [
        f"{FSM_PREFIX}:*:*:state",
        f"{FSM_PREFIX}:*:*:data",
    ]

    for pattern in patterns:
        for key in r.scan_iter(pattern):
            parsed = parse_fsm_key(key, FSM_PREFIX)

            if not parsed:
                continue

            chat_id = parsed["chat_id"]
            user_id = parsed["user_id"]
            key_type = parsed["key_type"]

            unique_key = (chat_id, user_id)

            if unique_key not in users:
                users[unique_key] = {
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "state": None,
                    "data": {},
                }

            value = r.get(key)

            if key_type == "state":
                users[unique_key]["state"] = value

            elif key_type == "data":
                try:
                    users[unique_key]["data"] = json.loads(value) if value else {}
                except json.JSONDecodeError:
                    users[unique_key]["data"] = {}

    return list(users.values())


# =========================
# ГЕНЕРАЦИЯ CSV
# =========================

def get_full_name(data: dict) -> str:
    name = str(data.get("name", "") or "").strip()
    surname = str(data.get("surname", "") or "").strip()

    if name and surname and surname not in name:
        return f"{name} {surname}"

    if name:
        return name

    if surname:
        return surname

    return ""


def normalize_activities(value):
    """
    registered_activities должен быть массивом.
    Но на всякий случай обрабатываем и строку.
    """

    if not value:
        return []

    if isinstance(value, str):
        value = [value]

    if not isinstance(value, list):
        return []

    result = []

    for item in value:
        item = str(item or "").strip()

        if item and item not in result:
            result.append(item)

    return result


def generate_activity_status_csv(users, filename: str):
    rows = []

    for user in users:
        data = user.get("data") or {}

        if not isinstance(data, dict):
            continue

        activities = normalize_activities(data.get("registered_activities"))

        if not activities:
            continue

        for activity in activities:
            rows.append({
                "Активность": activity,
                "Имя": get_full_name(data),
                "Telegram ID": user.get("user_id", ""),
                "Дата рождения": data.get("birth", ""),
                "Город": data.get("city", ""),
                "Email": data.get("email", ""),
                "Телефон": data.get("number", ""),
            })

    # Группировка по активности через сортировку
    rows.sort(
        key=lambda row: (
            str(row["Активность"]).lower(),
            str(row["Имя"]).lower(),
            str(row["Telegram ID"]),
        )
    )

    fieldnames = [
        "Активность",
        "Имя",
        "Telegram ID",
        "Дата рождения",
        "Город",
        "Email",
        "Телефон",
    ]

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            delimiter=";",
        )

        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


# =========================
# ХЕНДЛЕР
# =========================

@dp.message_handler(commands=["activity_status"], state="*")
async def activity_status_handler(message: types.Message, state: FSMContext):
    await message.answer("Формирую CSV по регистрациям на активности...")

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"activity_status_{now}.csv"

    try:
        users = get_all_bot_users()

        rows_count = generate_activity_status_csv(
            users=users,
            filename=filename,
        )

        if rows_count == 0:
            await message.answer("Регистраций на активности пока не найдено.")
            return

        await message.answer_document(
            document=types.InputFile(filename),
            caption=f"Готово. Регистраций найдено: {rows_count}",
        )

    except Exception as e:
        await message.answer(f"Ошибка при формировании отчета: {e}")

    finally:
        if os.path.exists(filename):
            os.remove(filename)
