from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMedit(StatesGroup):
    base_state = State()
    edit_user_state = State()