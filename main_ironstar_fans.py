from aiogram import executor
from handlers import *

from loader import dp
from db import init_db, close_db


async def on_startup(dispatcher):
    print("Starting Questern_ironstar_fans bot", flush=True)
    await init_db()
    print("DB connected", flush=True)


async def on_shutdown(dispatcher):
    await close_db()
    print("DB disconnected", flush=True)


if __name__ == "__main__":
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )