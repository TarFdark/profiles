from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor


TOKEN = ""
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

global editing_name
global editing_bio
editing_name,editing_bio = False,False



edit_name= KeyboardButton('Edit name')
edit_bio= KeyboardButton('Edit bio')
buttons = ReplyKeyboardMarkup()
buttons.add(edit_name, edit_bio)


@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    await msg.answer("Привет",reply_markup=buttons)


@dp.message_handler(content_types=['text'])
async def get_new(msg: types.Message):
    global editing_name
    global editing_bio
    if editing_name:
        #меняешь имя
        await msg.answer("Имя изменено",reply_markup=buttons)
        editing_name=False
    if editing_bio:
        # меняешь био
        await msg.answer("Био изменено", reply_markup=buttons)
        editing_bio = False

    if msg.text == "Edit name":
        await msg.answer("Введите новое имя", reply_markup=buttons)
        editing_name = True
    if msg.text == "Edit bio":
        await msg.answer("Введите новое био", reply_markup=buttons)
        editing_bio = True





if __name__ == '__main__':
   executor.start_polling(dp)

