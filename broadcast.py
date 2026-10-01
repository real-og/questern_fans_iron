import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import BotBlocked, ChatNotFound
from loader import bot, dp

def load_user_ids(filename="id.txt"):
    user_ids = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            user_ids.append(int(line))

    return user_ids



async def main():
    user_ids = load_user_ids("id.txt")


    user_ids = list(set(user_ids))


    text = """Привет 👋🏼 
Напоминаем, что вы зарегистрированы на тренировку по плаванию с Александром и Андреем Брюханковыми.

Обращаем внимание: в афише активности по техническим причинам была допущена ошибка — указана дата проведения 2 октября (пятница).
<b>Актуальная дата проведения — 1 октября (сегодня)</b>

Если вы не сможете посетить тренировку, пожалуйста, отмените регистрацию — сделать это можно по той же кнопке, через которую вы регистрировались.

До встречи!"""




    for user_id in user_ids:
        try:
            await bot.send_message(user_id, text)
            print(f"✅ Сообщение отправлено {user_id}")
            await asyncio.sleep(0.5)  # минимальная задержка, чтобы избежать спама
        except BotBlocked:
            print(f"⛔ Бот заблокирован пользователем {user_id}")
        except ChatNotFound:
            print(f"❌ Чат не найден для {user_id}")
        except Exception as e:
            print(f"⚠️ Ошибка при отправке {user_id}: {e}")

    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())