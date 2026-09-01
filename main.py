"""Точка входа."""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import cfg
from database import db
from handlers import user_router, moderator_router

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    await db.init()

    bot = Bot(token=cfg.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(moderator_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
