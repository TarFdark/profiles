from datetime import date
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo
from tgbot.states.EditByAdmin import EditByAdmin
from tgbot.utils.keyboards import get_users_keyboard, get_admin_edit_profile_keyboard, get_delete_user_keyboard


async def admin_menu(message: Message, repo: Repo):
    users = await repo.get_users()
    if not users:
        return await message.answer('Добавленных пользователей нет')

    await message.answer("Выберите пользователя", reply_markup=get_users_keyboard(users))


async def choose_action(call: CallbackQuery, state: FSMContext, repo: Repo):
    user_id = call.data.split('_')[-1]
    user = await repo.get_user_by_id(user_id)

    # вывод анкеты
    # мб вынести в функцию, т.к. используется и в обычной команде гета?
    media_group = []
    text = ''.join(
        [
            'ФИО' if user.patronymic else 'ФИ',
            f': {user.last_name} {user.first_name} {user.patronymic if user.patronymic else ""}\n',
            f'Дата рождения: {user.birthday}\n',
            f'Город: {user.city}\n',
            f'О себе: {user.bio}',
        ]
    )
    for i, image in enumerate(user.images):
        media_group.append(InputMediaPhoto(image.telegram_photo_id, caption=text if i == 0 else ''))
        
    await call.message.answer_media_group(media_group)

    await state.set_state(EditByAdmin.choose_action.state)
    await state.set_data({'user_id': user_id})

    await call.message.answer('Выберите действие', reply_markup=get_admin_edit_profile_keyboard())
    await call.answer()


async def edit_user_bio(call: CallbackQuery, state: FSMContext):
    await state.set_state(EditByAdmin.here_bio.state)
    await call.message.answer('Введите новое био (старое будет удалено без возможности восстановления)')
    await call.answer()


async def here_bio_edit_user(message: Message, state: FSMContext, repo: Repo):
    data = await state.get_data()
    user_id = data['user_id']

    await repo.update_user(id=user_id, bio=message.text)
    await message.answer('Данные были успешно обновлены')
    await state.finish()


async def delete_user(call: CallbackQuery):
    await call.message.answer('Вы уверены, что хотите полностью удалить профиль пользователя?', reply_markup=get_delete_user_keyboard())
    await call.answer()


async def deleting(call: CallbackQuery, state: FSMContext, repo: Repo):
    data = await state.get_data()
    user_id = data['user_id']

    await repo.delete_user(user_id)
    await call.message.answer('Анкета была успешно удалена')
    await call.answer()
    await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_menu, commands="admin", state="*", role=UserRole.ADMIN)
    dp.register_callback_query_handler(choose_action, Text(startswith='user'), role=UserRole.ADMIN)
    dp.register_callback_query_handler(edit_user_bio, Text('admin_edit_bio'), state=EditByAdmin.choose_action, role=UserRole.ADMIN)
    dp.register_message_handler(here_bio_edit_user, state=EditByAdmin.here_bio, role=UserRole.ADMIN)
    dp.register_callback_query_handler(delete_user, Text('admin_delete_profile'), state=EditByAdmin.choose_action, role=UserRole.ADMIN)
    dp.register_callback_query_handler(deleting, Text('delete_user'), state=EditByAdmin.choose_action, role=UserRole.ADMIN)
