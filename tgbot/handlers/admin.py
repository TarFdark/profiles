from datetime import date
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo
from db.pool_creater import create_pool


async def admin_start(message: Message):
    await message.reply("Hello, admin!")
    sm = await create_pool("profiles", False)
    repo = Repo(sm())


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", role=UserRole.ADMIN)
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
