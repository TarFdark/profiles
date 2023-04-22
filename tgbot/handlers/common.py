from aiogram import Dispatcher
from aiogram.types import Message


async def ping(message: Message):
    await message.reply("Pong!")


def register_main(dp: Dispatcher):
    dp.register_message_handler(ping, commands=["ping"], state="*")
