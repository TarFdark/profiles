from aiogram import types


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
