import logging

from typing import List
from datetime import date
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, UserImage


logger = logging.getLogger(__name__)


class Repo:
    """Db abstraction layer"""


    def __init__(self, conn):
        self.conn: AsyncSession = conn


    async def add_user(self, telegram_id: int, telegram_first_name: str, first_name: str, last_name: str, surname: str, birthday: date, city: str, bio: str, images: list[str], telegram_last_name: str = "") -> None:
        """Add new user to DB if doesn't exist

        Args:
            telegram_id (int): telegram user id
            telegram_first_name (str): telegram first name
            first_name (str): real-life first name
            last_name (str): real-life last name
            surname (str): real-life surname
            birthday (date): birthday
            city (str): city
            bio (str): hobbies and achievements
            images (list[str]): paths to user images (from 1 to 3 images allowed)
            telegram_last_name (str, optional): telegram last name. Defaults to "".
        """

        if not 1 <= len(images) <= 3:
            raise ValueError(f'Allowed from 1 to 3 images, not {len(images)}')

        user = User(
            telegram_id=telegram_id,
            telegram_link=f"tg://user?id={telegram_id}",
            telegram_name=telegram_first_name + telegram_last_name,
            first_name=first_name,
            last_name=last_name,
            surname=surname,
            birthday=birthday,
            city=city,
            bio=bio
        )
        self.conn.add(user)
        logger.info(f"add new user {user}")

        for image in images:
            user_image = UserImage(path=image, user=user)
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
