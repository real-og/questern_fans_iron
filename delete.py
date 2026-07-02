import json
from datetime import datetime

import redis


# =========================
# НАСТРОЙКИ REDIS
# =========================

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_PASSWORD = None

FSM_PREFIX = "fsm"


# =========================
# КОГО ЧИСТИМ
# =========================

TARGET_USER_IDS = {
    6167283093,
    6150574145,
    520251635,
}


# =========================
# КАКИЕ ПОЛЯ УДАЛЯЕМ
# =========================

REGISTRATION_FIELDS_TO_DELETE = [
    # "confirm_date",
    # "event_number",
    # "minsk_reg",
    # "fan_number",
    # "birth",
    # "city",
    # "email",
    "registered_activities",
]


def to_int_if_possible(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return value


def parse_fsm_key(key: str, prefix: str):
    """
    Ожидаемый формат RedisStorage2:
    fsm:<chat_id>:<user_id>:data
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


def main():
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True,
    )

    backup = []
    changed_count = 0
    found_user_ids = set()

    pattern = f"{FSM_PREFIX}:*:*:data"

    for key in r.scan_iter(pattern):
        parsed = parse_fsm_key(key, FSM_PREFIX)

        if not parsed:
            continue

        user_id = parsed["user_id"]

        if user_id not in TARGET_USER_IDS:
            continue

        found_user_ids.add(user_id)

        raw_value = r.get(key)

        if not raw_value:
            continue

        try:
            data = json.loads(raw_value)
        except json.JSONDecodeError:
            print(f"❌ Не удалось разобрать JSON в ключе: {key}")
            continue

        if not isinstance(data, dict):
            print(f"❌ Данные в ключе не dict: {key}")
            continue

        old_data = data.copy()

        deleted_fields = []

        for field in REGISTRATION_FIELDS_TO_DELETE:
            if field in data:
                deleted_fields.append(field)
                data.pop(field)

        if not deleted_fields:
            print(f"ℹ️ У пользователя {user_id} нечего удалять. Ключ: {key}")
            continue

        backup.append({
            "redis_key": key,
            "chat_id": parsed["chat_id"],
            "user_id": user_id,
            "old_data": old_data,
            "new_data": data,
            "deleted_fields": deleted_fields,
        })

        r.set(key, json.dumps(data, ensure_ascii=False))

        changed_count += 1

        print(f"✅ Очищен пользователь {user_id}")
        print(f"   Redis key: {key}")
        print(f"   Удалены поля: {', '.join(deleted_fields)}")

    backup_filename = f"registration_cleanup_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(backup_filename, "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=2)

    print()
    print("Готово.")
    print(f"Изменено записей: {changed_count}")
    print(f"Бэкап сохранен в файл: {backup_filename}")

    not_found = TARGET_USER_IDS - found_user_ids

    if not_found:
        print(f"Не найдены user_id в Redis data: {sorted(not_found)}")


if __name__ == "__main__":
    main()