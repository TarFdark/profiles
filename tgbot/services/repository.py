import logging

from typing import List
from datetime import date
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, UserImage


logger = logging.getLogger(__name__)


class Repo:
    """Db abstraction layer"""


    def __init__(self, conn):
        self.conn: AsyncSession = conn


    async def add_user(self, telegram_id: int, telegram_first_name: str, first_name: str, last_name: str, birthday: date, city: str, bio: str, images: list[str], telegram_last_name: str = "", patronymic: str = None) -> None:
        """Add new user to DB if doesn't exist

        Args:
            telegram_id (int): telegram user id
            telegram_first_name (str): telegram first name
            first_name (str): real-life first name
            last_name (str): real-life last name
            birthday (date): birthday
            city (str): city
            bio (str): hobbies and achievements
            images (list[str]): paths to user images (from 1 to 3 images allowed)
            telegram_last_name (str, optional): telegram last name. Defaults to "".
            patronymic (str, optional): real-life patronymic. Defaults to None.
        """
        if not 1 <= len(images) <= 3:
            raise ValueError(f'Allowed from 1 to 3 images, not {len(images)}')

        kwargs = {}
        if patronymic:
            kwargs['patronymic'] = patronymic

        user = User(
            telegram_id=telegram_id,
            telegram_link=f"tg://user?id={telegram_id}",
            telegram_name=f'{telegram_first_name} {telegram_last_name}',
            first_name=first_name,
            last_name=last_name,
            birthday=birthday,
            city=city,
            bio=bio,
            **kwargs
        )
        self.conn.add(user)
        logger.info(f"add new user {user}")

        for image in images:
            user_image = UserImage(telegram_photo_id=image, user=user)
            self.conn.add(user_image)
            logger.info(f"add new user image {user_image}")

        await self.conn.commit()


    async def get_users(self) -> List[User]:
        """List all user's forms

        Returns:
            List[User]: list of users
        """

        return [
            row 
            for row in await self.conn.execute(
                select(User)
            )
        ]


    async def get_user(self, telegram_id: int) -> User | None:
        """Return user by telegram id or None

        Args:
            telegram_id (int): telegram user id

        Returns:
            User | None: user object
        """

        res = await self.conn.execute(
            select(User).where(User.telegram_id == telegram_id).options(selectinload(User.images))
        )
        
        return res.scalars().first()
    

    async def update_user(self, telegram_id: int, **kwargs):
        user = await self.get_user(telegram_id)

        if not user:
            raise ValueError(f'User with id {telegram_id} doesn\'t exist')

        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError(f'Class `User` doesn\'t have argument {key}') 
            setattr(user, key, value)

        await self.conn.commit()


    async def add_user_photo(self, telegram_user_id: int, telegram_photo_id):
        user = await self.get_user(telegram_user_id)
        if not user:
            raise ValueError(f'User with id {telegram_user_id} doesn\'t exist')
        
        user_image = UserImage(telegram_photo_id=telegram_photo_id, user=user)
        self.conn.add(user_image)
        await self.conn.commit()


    async def delete_user_photos(self, telegram_user_id: int):
        user = await self.get_user(telegram_user_id)
        if not user:
            raise ValueError(f'User with id {telegram_user_id} doesn\'t exist')
        
        res = await self.conn.execute(
            select(UserImage).where(UserImage.user_id == user.id)
        )
        user_images = res.scalars().all()
        for img in user_images:
            await self.conn.delete(img)

        await self.conn.commit()
