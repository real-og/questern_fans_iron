from loader import db
from fan_id_interface import get_event_id

async def check_event_id(telegram_id, event_column) -> int:
    print(telegram_id)
    user = await db.get(telegram_id)

    if not user:
        raise ValueError("Пользователь не найден")

    # Если event_id уже есть
    current_event_id = str(user.get(event_column, "")).strip()

    if current_event_id.isdigit():
        return int(current_event_id)

    # Если нет — определяем новый
    all_users = await db.get_all()

    new_event_id = get_event_id(
        all_users,
        event_column
    )

    # Записываем пользователю
    await db.update(
        telegram_id,
        **{event_column: new_event_id}
    )

    return new_event_id