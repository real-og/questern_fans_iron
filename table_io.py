import csv
import os
import asyncio
from tempfile import NamedTemporaryFile


class CSVDatabase:
    def __init__(self, filename: str, id_field: str = "telegram_id"):
        self.filename = filename
        self.id_field = id_field
        self.lock = asyncio.Lock()

    def _read(self):
        with open(self.filename, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return reader.fieldnames, list(reader)

    def _write(self, fieldnames, rows):
        # Сначала пишем во временный файл.
        # Только после успешной записи заменяем основной.
        with NamedTemporaryFile(
            "w",
            delete=False,
            encoding="utf-8-sig",
            newline="",
            dir=os.path.dirname(self.filename) or "."
        ) as tmp:

            writer = csv.DictWriter(tmp, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

            temp_name = tmp.name

        os.replace(temp_name, self.filename)

    async def add(self, data: dict):
        async with self.lock:
            fields, rows = self._read()

            telegram_id = str(data[self.id_field])

            if any(str(row[self.id_field]) == telegram_id for row in rows):
                raise ValueError(f"{self.id_field}={telegram_id} уже существует")

            # Не разрешаем случайно записать неизвестные колонки
            unknown = set(data) - set(fields)
            if unknown:
                raise ValueError(f"Неизвестные поля: {unknown}")

            new_row = {field: data.get(field, "") for field in fields}
            rows.append(new_row)

            self._write(fields, rows)

    async def update(self, telegram_id, **changes):
        async with self.lock:
            fields, rows = self._read()

            unknown = set(changes) - set(fields)
            if unknown:
                raise ValueError(f"Неизвестные поля: {unknown}")

            telegram_id = str(telegram_id)

            for row in rows:
                if str(row[self.id_field]) == telegram_id:
                    for key, value in changes.items():
                        row[key] = value

                    self._write(fields, rows)
                    return

            raise ValueError(f"Пользователь {telegram_id} не найден")

    async def get(self, telegram_id):
        async with self.lock:
            _, rows = self._read()

            telegram_id = str(telegram_id)

            for row in rows:
                if str(row[self.id_field]) == telegram_id:
                    return row

            return None
        
    async def get_all(self):
        async with self.lock:
            _, rows = self._read()
            return rows
        


