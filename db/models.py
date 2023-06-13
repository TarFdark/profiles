from datetime import datetime
from typing import List
from sqlalchemy import Column, BigInteger, Integer, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship


from db.base import Base


class BaseCommon(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class User(BaseCommon):    
    __tablename__ = "users"

    telegram_id = Column(BigInteger)
    telegram_link = Column(Text)                    # tg://user?id=<telegram_id>
    telegram_name = Column(Text)                    # firstname + (" " + lastname if lastname else "")

    # fill by user
    last_name = Column(Text)
    first_name = Column(Text)
    patronymic = Column(Text, nullable=True)
    birthday = Column(Date)
    city = Column(Text)
    bio = Column(Text)

    images = relationship("UserImage", backref='user')

    def __repr__(self):
        return (
            f'User(telegram_id={self.telegram_id}, telegram_link="{self.telegram_link}", telegram_name="{self.telegram_name}", '
            f'first_name="{self.first_name}", last_name="{self.last_name}", patronymic="{self.patronymic}", birthday={self.birthday}, city="{self.city}", bio="{self.bio}")'
        )


class UserImage(BaseCommon):
    __tablename__ = "user_images"

    telegram_photo_id = Column(Text)

    user_id = Column(BigInteger, ForeignKey('users.id'))

    def __repr__(self):
        return f'UserImage(telegram_photo_id="{self.telegram_photo_id}"'