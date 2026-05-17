from tortoise import fields
from tortoise.models import Model


class User(Model):
    user_id = fields.IntField(primary_key=True)

    first_name = fields.CharField(max_length=100, null=True)
    last_name = fields.CharField(max_length=100, null=True)
    phone = fields.CharField(max_length=30, null=True)
    telegram_id = fields.BigIntField(unique=True, null=True)
    max_id = fields.CharField(max_length=100, null=True)
    fan_number = fields.CharField(max_length=100, unique=True, null=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"


class BotSection(Model):
    section_id = fields.IntField(primary_key=True)

    button_name = fields.CharField(max_length=255)
    content_text = fields.TextField(null=True)
    file_name = fields.CharField(max_length=500, null=True)
    is_shown = fields.BooleanField(default=True)

    class Meta:
        table = "bot_sections"


class UserAction(Model):
    action_id = fields.BigIntField(primary_key=True)

    user = fields.ForeignKeyField(
        "models.User",
        related_name="actions",
        source_field="user_id",
    )

    section = fields.ForeignKeyField(
        "models.BotSection",
        related_name="actions",
        source_field="section_id",
    )

    executed_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_actions"