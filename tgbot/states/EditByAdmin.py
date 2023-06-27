from aiogram.dispatcher.filters.state import State, StatesGroup


class EditByAdmin(StatesGroup):
    choose_action = State()
    here_bio = State()
