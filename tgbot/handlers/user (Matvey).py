from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor


TOKEN = ""
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

global editing_name
editing_name=False
global editing_bio
editing_bio=False


edit_name= KeyboardButton('/Edit_name')
edit_bio= KeyboardButton('/Edit_bio')
buttons = ReplyKeyboardMarkup()
buttons.add(edit_name, edit_bio)


@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    await msg.answer("Привет",reply_markup=buttons)

@dp.message_handler(commands=['Edit_name'])
async def edit_name(msg: types.Message):
    global editing_name
    editing_name=True
    await msg.answer("Введите новое имя",reply_markup=buttons)

@dp.message_handler(commands=['Edit_bio'])
async def edit_bio(msg: types.Message):
    global editing_bio
    editing_bio = True
    await msg.answer("Введите новое био", reply_markup=buttons)

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





if __name__ == '__main__':
   executor.start_polling(dp)

