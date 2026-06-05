import redis


redis_client = redis.Redis(
    host="127.0.0.1",
    port=6379,
    db=1,
    decode_responses=True,
)

FAN_ID_KEY = "next_fan_id"
FAN_NUMBER_KEY = "next_fan_number"


def get_fan_id() -> int:
    """
    Возвращает новый уникальный номер болельщика.
    Номера идут по порядку и сохраняются после перезапуска бота.
    """

    new_id = redis_client.incr(FAN_ID_KEY)

    return new_id

def get_fan_number() -> int:
    new_number = redis_client.incr(FAN_NUMBER_KEY)
    return new_number