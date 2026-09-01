"""Конфигурация бота."""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, slots=True)
class Config:
    """Конфигурационные параметры."""

    bot_token: str
    admin_ids: set[int]
    group_chat_id: int | None
    db_path: str = "looksmaxing.db"


def load_config() -> Config:
    """Загрузить конфигурацию из переменных окружения."""
    token = os.getenv("BOT_TOKEN", "")
    admin_ids_raw = os.getenv("ADMIN_IDS", "")
    group_chat_id_raw = os.getenv("GROUP_CHAT_ID", "")

    admin_ids = {int(x.strip()) for x in admin_ids_raw.split(",") if x.strip()}
    group_chat_id = int(group_chat_id_raw) if group_chat_id_raw else None

    return Config(
        bot_token=token,
        admin_ids=admin_ids,
        group_chat_id=group_chat_id,
    )


cfg = load_config()
