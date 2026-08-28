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


    text = """<i>Привет, друг!</i>
Команда IRONSTAR напоминает: уже сегодня вечером встречаемся на <b>SUNSET RUN</b>🌅
Сбор в <b>18:30</b>, 5К в <b>19:00</b>, розыгрыш 10 подарков в <b>20:00</b>.

А уже в субботу приглашаем на забеги <b>IRONLADY</b> и <b>MANSTAR</b> — 
для участников SUNSET RUN подготовили специальный промокод <b><a href="https://iron-star.com/event/f/city-is-nizhniy-novgorod/">RUNN20 на скидку 20%</a></b>.

<i>До встречи!⚡️</i>"""




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