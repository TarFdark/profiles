import asyncio
import logging

from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from db import create_db
from config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user
from tgbot.handlers.common import register_main
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware
from db.models import BaseCommon
from db.pool_creater import create_pool

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/ping", description="Проверить отклик бота")
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config("config.ini")

    storage = MemoryStorage()
    pool: sessionmaker = await create_pool(
        database=config.db.database,
        echo=False,
    )

    bot = Bot(token=config.tg_bot.token)
    await set_commands(bot)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_user(dp)
    register_main(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
