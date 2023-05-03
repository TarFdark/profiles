from aiogram.bot import bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.exceptions import MessageNotModified
from aiogram import Bot



async def main_edit_mes(text: str, ikb: InlineKeyboardMarkup, call=None, message_id: int = None, chat_id: int = None,) -> None:
    if chat_id == None and message_id == None and call != None:
        message_id = call.message.message_id
        chat_id = call.message.chat.id
    try:
        await Bot.edit_message_text(
            text=text,
            message_id=message_id,
            chat_id=chat_id,
            reply_markup=ikb,
            parse_mode='html')
    except MessageNotModified:
        pass