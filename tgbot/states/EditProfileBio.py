from aiogram.dispatcher.filters.state import State, StatesGroup


class EditProfileBio(StatesGroup):
    here_new_bio = State()
