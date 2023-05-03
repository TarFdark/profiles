from datetime import date
from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from func_bot import main_edit_mes
from tgbot.models.role import UserRole
from tgbot.services.repository import Repo
from db.pool_creater import create_pool

import keyboards
from state.state_admin import FSMedit


async def admin_start(message: Message, bot:Bot):
    await bot.send_message(message.from_user.id,
                           f"Добро пожаловать {message.from_user.first_name}", reply_markup=keyboards.kb_menu)

async def search_change_profile(call, state:FSMContext):
    await FSMedit.base_state.set()
    # get a list of all user ids from the database and the names
    # of all users from the database
    rec_id = [] # list all id users
    rec_names = [] # list all name users
    step, cur_step = 10, 0
    ikb = keyboards.create_ikb_records_list(rec_id, rec_names, step=step, cur_step=cur_step)
    text = "Выберите пользователя которого хотите изменить Страница 1 "
    await main_edit_mes(text=text, call=call, ikb=ikb)
    async with state.proxy() as data:
        data["next_inline"] = [step, cur_step, rec_id, rec_names]


async def next_search_profile(call, state:FSMContext):
    async with state.proxy() as data:
        [step, cur_step, rec_id, rec_names] = data["next_inline"]
    diff = 10 if call.data == "next_inline" else -10
    step += diff
    cur_step += diff
    ikb = keyboards.create_ikb_records_list(rec_id, rec_names, step=step, cur_step=cur_step)
    text = f"Выберите пользователя которого хотите изменить Страница {step // 10}"
    await main_edit_mes(text=text, call=call, ikb=ikb)
    async with state.proxy() as data:
        data["next_inline"] = [step, cur_step, rec_id, rec_names]


async def get_info_user(call, state:FSMContext):
    data = call.data.split("_")[1:]
    id_user, name_user = data
    lsit_info_user = [] #get info user [bio, name, tg_name ...]
    text = "\n".join(lsit_info_user)
    await main_edit_mes(text=text, call=call, ikb=keyboards.kb_edit)
    async with state.proxy() as data:
        data["back_inline"] = call.data
        data["list_info_user"] = lsit_info_user


async def edit_element_user(call, state:FSMContext):
    async with state.proxy() as data:
       cd_data = data["back_inline"]
    element_edit = call.data.split('_')[-1]
    text = f"Введите новое значение для {element_edit} пользователя"
    ikb = keyboards.back_info_user(cd_data)
    await main_edit_mes(text=text, call=call, ikb=ikb)
    await FSMedit.edit_user_state.set()
    async with state.proxy() as data:
        data["element_edit"] = element_edit
        data["message_id"] = call.message.message_id
        data["chat_id"] = call.message.chat.id



async def input_edit_user(message:Message, state:FSMContext, bot:Bot):
    async with state.proxy() as data:
        element_edit = data["element_edit"]
        message_id = data["message_id"]
        chat_id = data["chat_id"]
    info_element = "" #get element information from database
    info_element_text = info_element
    if len(info_element_text) > 20:
        info_element_text = info_element[:20] + "..."
    text = f"Вы точно хотите изменить {info_element_text} на {message.text}"
    ikb = keyboards.kb_accept_and_reject_edit
    await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
    await main_edit_mes(text=text, message_id=message_id, chat_id=chat_id, ikb=ikb)
    async with state.proxy() as data:
        data["info_element"] = info_element



async def save_edit_user(call, state:FSMContext):
    async with state.proxy() as data:
        info_element = data["info_element"]
        element_edit = data["element_edit"]
    data = call.data.split("_")[0]
    if data == "accept":
        pass
    #change data in database  element_edit
    async with state.proxy() as data:
        lsit_info_user = data["list_info_user"]
    text = "\n".join(lsit_info_user)
    await main_edit_mes(text=text, call=call, ikb=keyboards.kb_edit)
    await FSMedit.base_state.set()

import keyboards
from state.state_admin import FSMedit


async def admin_start(message: Message, bot:Bot):
    await bot.send_message(message.from_user.id,
                           f"Добро пожаловать {message.from_user.first_name}", reply_markup=keyboards.kb_menu)

async def search_change_profile(call, state:FSMContext):
    await FSMedit.base_state.set()
    # get a list of all user ids from the database and the names
    # of all users from the database
    rec_id = [] # list all id users
    rec_names = [] # list all name users
    step, cur_step = 10, 0
    ikb = keyboards.create_ikb_records_list(rec_id, rec_names, step=step, cur_step=cur_step)
    text = "Выберите пользователя которого хотите изменить Страница 1 "
    await main_edit_mes(text=text, call=call, ikb=ikb)
    async with state.proxy() as data:
        data["next_inline"] = [step, cur_step, rec_id, rec_names]


async def next_search_profile(call, state:FSMContext):
    async with state.proxy() as data:
        [step, cur_step, rec_id, rec_names] = data["next_inline"]
    diff = 10 if call.data == "next_inline" else -10
    step += diff
    cur_step += diff
    ikb = keyboards.create_ikb_records_list(rec_id, rec_names, step=step, cur_step=cur_step)
    text = f"Выберите пользователя которого хотите изменить Страница {step // 10}"
    await main_edit_mes(text=text, call=call, ikb=ikb)
    async with state.proxy() as data:
        data["next_inline"] = [step, cur_step, rec_id, rec_names]


async def get_info_user(call, state:FSMContext):
    data = call.data.split("_")[1:]
    id_user, name_user = data
    lsit_info_user = [] #get info user [bio, name, tg_name ...]
    text = "\n".join(lsit_info_user)
    await main_edit_mes(text=text, call=call, ikb=keyboards.kb_edit)
    async with state.proxy() as data:
        data["back_inline"] = call.data
        data["list_info_user"] = lsit_info_user


async def edit_element_user(call, state:FSMContext):
    async with state.proxy() as data:
       cd_data = data["back_inline"]
    element_edit = call.data.split('_')[-1]
    text = f"Введите новое значение для {element_edit} пользователя"
    ikb = keyboards.back_info_user(cd_data)
    await main_edit_mes(text=text, call=call, ikb=ikb)
    await FSMedit.edit_user_state.set()
    async with state.proxy() as data:
        data["element_edit"] = element_edit
        data["message_id"] = call.message.message_id
        data["chat_id"] = call.message.chat.id



async def input_edit_user(message:Message, state:FSMContext, bot:Bot):
    async with state.proxy() as data:
        element_edit = data["element_edit"]
        message_id = data["message_id"]
        chat_id = data["chat_id"]
    info_element = "" #get element information from database
    info_element_text = info_element
    if len(info_element_text) > 20:
        info_element_text = info_element[:20] + "..."
    text = f"Вы точно хотите изменить {info_element_text} на {message.text}"
    ikb = keyboards.kb_accept_and_reject_edit
    await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
    await main_edit_mes(text=text, message_id=message_id, chat_id=chat_id, ikb=ikb)
    async with state.proxy() as data:
        data["info_element"] = info_element



async def save_edit_user(call, state:FSMContext):
    async with state.proxy() as data:
        info_element = data["info_element"]
        element_edit = data["element_edit"]
    data = call.data.split("_")[0]
    if data == "accept":
        pass
    #change data in database  element_edit
    async with state.proxy() as data:
        lsit_info_user = data["list_info_user"]
    text = "\n".join(lsit_info_user)
    await main_edit_mes(text=text, call=call, ikb=keyboards.kb_edit)
    await FSMedit.base_state.set()




def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", role=UserRole.ADMIN)
    dp.callback_query_handler(search_change_profile, lambda call: call.data )
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
