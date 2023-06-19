from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from tgbot.states.FillProfile import FillProfile
from tgbot.services.repository import Repo
from tgbot.utils.keyboards import get_fill_profile_keyboard


async def start(message: Message):
    await message.answer('start msg')


async def fill_profile(message: Message, state: FSMContext):
    await message.answer('Хорошо! Начинаем заполнение анкеты полностью. Введите ФИО полностью (отчество необязательно)')
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
    await message.answer('Введите город')
    await FillProfile.next()


async def fill_profile_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer('Введите описание о себе (чем занимаешься по жизни, достижения)')
    await FillProfile.next()


async def fill_profile_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text, photos=[])
    await message.answer('Отправьте от 1 до 3 фото для профиля', reply_markup=get_fill_profile_keyboard())
    await FillProfile.next()


async def fill_profile_photo(message: Message, state: FSMContext):
    print(message.photo)
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
    except BaseException:
        return await call.message.answer('Возникла неожиданная ошибка! Попробуйте еще раз')
    
    await call.message.answer('Анкета успешно добавлена')


async def get_profile(message: Message, state: FSMContext, repo: Repo):
    if message.reply_to_message is None:
        return await message.answer('Для использования этой команды, отправьте ее в ответ на сообщения участника, чью анкету надо просмотреть')
    
    user = await repo.get_user(message.reply_to_message.from_id)

    if user is None:
        return await message.answer('Анкеты этого пользователя нет в боте ¯\_(ツ)_/¯')
    
    media_group = []
    text = ''.join(
        [
            'ФИО' if user.patronymic else 'ФИ',
            f': {user.first_name} {user.last_name} {user.patronymic}\n',
            f'Дата рождения: {user.birthday}\n',
            f'Город: {user.city}\n',
            f'О себе: {user.bio}\n',
        ]
    )
    for i, image in enumerate(user.images):
        media_group.append(InputMediaPhoto(image.telegram_photo_id, caption=text if i == 0 else ''))
        
    await message.answer_media_group(media_group)


def register_main(dp: Dispatcher):
    dp.register_message_handler(fill_profile, commands="fill_profile", state="*")
    dp.register_message_handler(fill_profile_full_name, state=FillProfile.here_full_name)
    dp.register_message_handler(fill_profile_birthday, state=FillProfile.here_birthday)
    dp.register_message_handler(fill_profile_city, state=FillProfile.here_city)
    dp.register_message_handler(fill_profile_bio, state=FillProfile.here_bio)
    dp.register_message_handler(fill_profile_photo, state=FillProfile.here_photo, content_types=['photo'])
    dp.register_callback_query_handler(apply_fill_profile, Text('apply_photos'), state=FillProfile.here_photo)

    dp.register_message_handler(get_profile, commands="get_profile", state="*")
