from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts
import tables
from aiogram.types import InputFile
from states import State
import loader
import keyboards as kb
from aiogram.types import ReplyKeyboardRemove
import os

CONTENT_DIR = 'files'

def _chunk_text(text: str, limit: int = 3500):

    parts = []
    buf = []
    size = 0
    for line in text.splitlines(True):
        if size + len(line) > limit and buf:
            parts.append("".join(buf))
            buf, size = [], 0
        buf.append(line)
        size += len(line)
    if buf:
        parts.append("".join(buf))
    return parts


@dp.message_handler(commands=['add'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
   await message.answer("Пришлите сюда файл, который положить на сервер. Чтобы выйти, используйте команду /start")
   await State.adding.set()


@dp.message_handler(state=State.adding)
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer("Пришлите сюда файл, который положить на сервер. Чтобы выйти, используйте команду /start")


@dp.message_handler(state=State.adding, content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message, state: FSMContext):
    doc: types.Document = message.document
    filename = doc.file_name or f"{doc.file_unique_id}"
    save_path = os.path.join(CONTENT_DIR, filename)
    await doc.download(destination_file=save_path)
    await message.reply(f"✅ Сохранено: {save_path}")
    await message.answer("Можете прислать еще файл для загрузки на сервер. Чтобы выйти, используйте команду /start")
    


@dp.message_handler(commands=['items'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    items = []
    for name in sorted(os.listdir(CONTENT_DIR)):
        path = os.path.join(CONTENT_DIR, name)
        if os.path.isfile(path):
            items.append(name)

    if not items:
        await message.reply("Файлы отсутствуют.")
        return

    text = "Файлы на сервере:\n" + "\n".join(f"• {x}" for x in items)
    for part in _chunk_text(text):
        await message.answer(part)