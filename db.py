import asyncio
import os
import ssl
from pathlib import Path
from typing import Optional

from tortoise import Tortoise
from tortoise.exceptions import IntegrityError

import config_io
from models import User, BotSection, UserAction


BASE_DIR = Path(__file__).resolve().parent


def _get_config_value(key: str, default=None):
    value = config_io.get_value(key)
    if value is None or value == "":
        return default
    return value


def _make_ssl_context() -> ssl.SSLContext:
    ca_path = _get_config_value("DB_SSL_CA", "ca.crt")

    ca_path = Path(ca_path)

    if not ca_path.is_absolute():
        ca_path = BASE_DIR / ca_path

    if not ca_path.exists():
        raise FileNotFoundError(
            f"Не найден CA-сертификат MySQL: {ca_path}"
        )

    ssl_ctx = ssl.create_default_context(cafile=str(ca_path))
    ssl_ctx.check_hostname = True
    ssl_ctx.verify_mode = ssl.CERT_REQUIRED

    return ssl_ctx


async def init_db():
    host = _get_config_value("DB_HOST")
    port = int(_get_config_value("DB_PORT", 3306))
    user = _get_config_value("DB_USER")
    password = _get_config_value("DB_PASSWORD")
    db_name = _get_config_value("DB_NAME")

    ssl_ctx = _make_ssl_context()

    await Tortoise.init(
        config={
            "connections": {
                "default": {
                    "engine": "tortoise.backends.mysql",
                    "credentials": {
                        "host": host,
                        "port": port,
                        "user": user,
                        "password": password,
                        "database": db_name,

                        "charset": "utf8mb4",
                        "minsize": 1,
                        "maxsize": 1,
                        "connect_timeout": 10,

                        "ssl": ssl_ctx,
                    },
                }
            },
            "apps": {
                "models": {
                    "models": ["models"],
                    "default_connection": "default",
                }
            },
        },
        _enable_global_fallback=True,
    )

    conn = Tortoise.get_connection("default")

    await asyncio.wait_for(
        conn.execute_query("SELECT 1"),
        timeout=15,
    )

    print("DB real connection OK", flush=True)


async def close_db():
    await Tortoise.close_connections()


async def upsert_user(
    telegram_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    phone: Optional[str] = None,
    max_id: Optional[str] = None,
    fan_number: Optional[str] = None,
) -> User:
    user = await User.get_or_none(telegram_id=telegram_id)

    if user is None:
        try:
            return await User.create(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                max_id=max_id,
                fan_number=fan_number,
            )
        except IntegrityError:
            user = await User.get(telegram_id=telegram_id)

    update_fields = []

    data = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "max_id": max_id,
        "fan_number": fan_number,
    }

    for field_name, value in data.items():
        if value is not None and getattr(user, field_name) != value:
            setattr(user, field_name, value)
            update_fields.append(field_name)

    if update_fields:
        await user.save(update_fields=update_fields)

    return user


async def get_visible_bot_sections() -> list[BotSection]:
    return await BotSection.filter(is_shown=True).order_by("section_id")


async def get_bot_section(section_id: int) -> Optional[BotSection]:
    return await BotSection.get_or_none(
        section_id=section_id,
        is_shown=True,
    )


async def add_user_action(user_id: int, section_id: int) -> UserAction:
    return await UserAction.create(
        user_id=user_id,
        section_id=section_id,
    )