from aiogram.dispatcher.filters.state import State, StatesGroup


class FillProfile(StatesGroup):
    here_full_name = State()
    here_birthday = State()
    here_city = State()
    here_bio = State()
    here_photo = State()