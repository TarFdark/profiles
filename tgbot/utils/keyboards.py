from aiogram import types

from db.models import User


def get_user_actions_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.resize_keyboard = True
    buttons = [
        types.KeyboardButton('Заполнить профиль'),
        types.KeyboardButton('Изменить профиль'),
    ]
    keyboard.add(*buttons)
    return keyboard


def get_empty_keyboard() -> types.ReplyKeyboardRemove:
    return types.ReplyKeyboardRemove()


def get_fill_profile_keyboard(callback: str) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text='Готово', callback_data=f'apply_{callback}'),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_edit_profile_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text='Био', callback_data='edit_bio'),
        types.InlineKeyboardButton(text='Фотографии', callback_data='edit_photos'),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_users_keyboard(users: list[User]) -> types.InlineKeyboardMarkup:
    buttons = []
    for user in users:
        buttons.append(types.InlineKeyboardButton(text=f'{user.first_name[0]}. {user.last_name}', callback_data=f'user_{user.id}'))

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_admin_edit_profile_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text='Изменить био', callback_data='admin_edit_bio'),
        types.InlineKeyboardButton(text='Удалить анкету', callback_data='admin_delete_profile'),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_delete_user_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text='Удаляем', callback_data='delete_user'),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard