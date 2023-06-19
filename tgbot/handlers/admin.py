from datetime import date
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo


async def admin_start(message: Message):
    await message.reply("admin start text")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", role=UserRole.ADMIN)