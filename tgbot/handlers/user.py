from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.repository import Repo


async def user_start(message: Message, repo: Repo):
    await repo.add_user(message.from_user.id)
    await message.reply("Hello, user!")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
