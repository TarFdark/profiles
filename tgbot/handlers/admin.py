from datetime import date
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo


async def admin_menu(message: Message, repo: Repo):
    await message.reply("Выберите пользователя для ")


def register_admin(dp: Dispatcher):
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=UserRole.ADMIN)
    pass