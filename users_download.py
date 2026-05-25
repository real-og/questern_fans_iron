import json
import redis


REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_PASSWORD = None

FSM_PREFIX = "fsm"  # стандартный prefix у RedisStorage2


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

    # Берем и state, и data, потому что у пользователя может быть только одно из них
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
                    users[unique_key]["data"] = value

    return list(users.values())


if __name__ == "__main__":
    users = get_all_bot_users()

    print(f"Найдено пользователей: {len(users)}")

    for user in users:
        print(user)

    # Если нужно сохранить в файл
    with open("bot_users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)