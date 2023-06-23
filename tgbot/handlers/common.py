import logging

from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from tgbot.states.FillProfile import FillProfile
from tgbot.states.EditProfileBio import EditProfileBio
from tgbot.states.EditProfilePhotos import EditProfilePhotos
from tgbot.services.repository import Repo
from tgbot.utils.keyboards import get_fill_profile_keyboard, get_edit_profile_keyboard, get_user_actions_keyboard, get_empty_keyboard


logger = logging.getLogger(__name__)


async def start(message: Message, state: FSMContext):
    await message.answer('Старт юзер месседж сука!', reply_markup=get_user_actions_keyboard())
    await state.finish()


async def cancel(message: Message, state: FSMContext):
    await message.answer('Командна отменена')
    await state.finish()


async def fill_profile(message: Message, state: FSMContext, repo: Repo):
    user = await repo.get_user(message.from_id)
    if user:
        await message.answer('У вас уже добавлена анкета, при продолжении прошлые данные будут удалены без возможности восстановления! Для отмены, используйте команду /cancel.')

    await message.answer('Введите ФИО полностью (отчество необязательно)', reply_markup=get_empty_keyboard())
    await state.set_state(FillProfile.here_full_name.state)


async def fill_profile_full_name(message: Message, state: FSMContext):
    full_name = message.text.split()
    if len(full_name) not in (2, 3): 
        return await message.answer('Неверный формат!')

    #    0     1     2
    # Фамилия Имя Отчество 
    data = {
        "last_name": full_name[0],
        "first_name": full_name[1],
        "patronymic": None
    }
    if len(full_name) == 3:
        data["patronymic"] = full_name[2]

    await state.set_data(data)
    await message.answer('Введите дату рождения в формате dd.mm.yyyy (например, 02.12.2003)')
    await FillProfile.next()


async def fill_profile_birthday(message: Message, state: FSMContext):
    try:
        birthday = datetime.strptime(message.text, '%d.%m.%Y')
    except ValueError:
        return await message.answer('Неверный формат!')

    await state.update_data(birthday=birthday)
    await message.answer('Введите место проживания')
    await FillProfile.next()


async def fill_profile_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer('Введите описание о себе (чем занимаешься по жизни, достижения)')
    await FillProfile.next()


async def fill_profile_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text, photos=[])
    await message.answer('Отправьте от 1 до 3 фото для профиля', reply_markup=get_fill_profile_keyboard('new_profile_photos'))
    await FillProfile.next()


async def fill_profile_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data["photos"]
    if len(photos) > 3:
        return await message.answer('Вы уже добавили макс. количество фото')
    
    photo_id = max(message.photo, key=lambda x: x.height).file_id
    photos.append(photo_id)
    await state.update_data(photos=photos)


async def apply_fill_profile(call: CallbackQuery, state: FSMContext, repo: Repo):
    await call.answer()

    data = await state.get_data()

    if not (1 <= len(data["photos"]) <= 3):
        return await call.message.answer(f'Необходимо добавить от 1 до 3 фото, не {len(data["photos"])} шт.')

    try:
        await repo.add_user(
            telegram_id=call.from_user.id,
            telegram_first_name=call.from_user.first_name,
            first_name=data["first_name"],
            last_name=data["last_name"],
            patronymic=data["patronymic"],
            birthday=data["birthday"],
            city=data["city"],
            bio=data["bio"],
            images=data["photos"],
            telegram_last_name="" if call.from_user.last_name is None else call.from_user.last_name
        )
    except BaseException as e:
        logger.error(e)
        return await call.message.answer('Возникла неожиданная ошибка! Попробуйте еще раз')
    
    await call.message.answer('Анкета успешно добавлена')


async def get_profile(message: Message, state: FSMContext, repo: Repo):
    if message.reply_to_message is None:
        return await message.answer('Для использования этой команды, отправьте ее в ответ на сообщения участника, чью анкету надо просмотреть')
    
    user = await repo.get_user(message.reply_to_message.from_id)

    if not user:
        return await message.answer('Анкеты этого пользователя нет в боте ¯\_(ツ)_/¯')
    
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
        
    await message.answer_media_group(media_group)


async def edit_profile(message: Message, repo: Repo):
    user = await repo.get_user(message.from_id)

    if not user:
        return await message.answer('Вашей анкеты нет в боте', reply_markup=get_empty_keyboard())
    
    await message.answer(
        'Выберите параметр, который необходимо изменить. Остальные параметры (имя, город и т.д.) можно изменить только при повторном полном заполнении анкеты (/fill_profile)',
        reply_markup=get_edit_profile_keyboard()
    )


async def edit_profile_bio(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Введите новое био (старое будет удалено без возможности восстановления)')
    await state.set_state(EditProfileBio.here_new_bio.state)


async def here_bio_edit_profile(message: Message, state: FSMContext, repo: Repo):
    await repo.update_user(message.from_id, bio=message.text)
    await message.answer('Данные были успешно обновлены')
    await state.finish()


async def edit_profile_photos(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Отправьте от 1 до 3 фото для профиля (старые будут удалены без возможности восстановления)', reply_markup=get_fill_profile_keyboard('update_profile_photos'))
    await state.set_state(EditProfilePhotos.here_photo.state)
    await state.update_data(photos=[])


async def here_photos_edit_profile(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data["photos"]
    if len(photos) > 3:
        return await message.answer('Вы уже добавили макс. количество фото')
    
    photo_id = max(message.photo, key=lambda x: x.height).file_id
    photos.append(photo_id)
    await state.update_data(photos=photos)

    
async def apply_update_profile_photos(call: CallbackQuery, state: FSMContext, repo: Repo):
    data = await state.get_data()
    photos = data["photos"]

    if not (1 <= len(photos) <= 3):
        return await call.message.answer(f'Необходимо добавить от 1 до 3 фото, не {len(photos)} шт.')
    
    await repo.delete_user_photos(call.from_user.id)
    for photo in photos:
        await repo.add_user_photo(call.from_user.id, photo)

    await call.message.answer('Фото успешно обновлены')


def register_main(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(cancel, commands="cancel", state="*")

    dp.register_message_handler(fill_profile, Text("Заполнить профиль"), state="*")
    dp.register_message_handler(fill_profile_full_name, state=FillProfile.here_full_name)
    dp.register_message_handler(fill_profile_birthday, state=FillProfile.here_birthday)
    dp.register_message_handler(fill_profile_city, state=FillProfile.here_city)
    dp.register_message_handler(fill_profile_bio, state=FillProfile.here_bio)
    dp.register_message_handler(fill_profile_photo, state=FillProfile.here_photo, content_types=['photo'])
    dp.register_callback_query_handler(apply_fill_profile, Text('apply_new_profile_photos'), state=FillProfile.here_photo)

    dp.register_message_handler(get_profile, commands="get_profile", state="*")

    dp.register_message_handler(edit_profile, Text("Изменить профиль"), state="*")
    dp.register_callback_query_handler(edit_profile_bio, Text('edit_bio'), state='*')
    dp.register_message_handler(here_bio_edit_profile, state=EditProfileBio.here_new_bio)
    dp.register_callback_query_handler(edit_profile_photos, Text('edit_photos'), state='*')
    dp.register_message_handler(here_photos_edit_profile, state=EditProfilePhotos.here_photo, content_types=['photo'])
    dp.register_callback_query_handler(apply_update_profile_photos, Text('apply_update_profile_photos'), state=EditProfilePhotos.here_photo)
