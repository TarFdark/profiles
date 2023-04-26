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

    telegram_id     = Column(BigInteger)
    telegram_link   = Column(Text)                    # tg://user?id=<telegram_id>
    telegram_name   = Column(Text)                    # firstname + (" " + lastname if lastname else "")

    # fill by user
    first_name  = Column(Text)
    last_name   = Column(Text)
    surname     = Column(Text)
    birthday    = Column(Date)
    city        = Column(Text)
    bio         = Column(Text)

    images = relationship("UserImage", backref='user')

    def __repr__(self):
        return f'User({self.id = }, {self.telegram_id = }, {self.telegram_link = }, {self.telegram_name = }, {self.first_name = }, {self.last_name}, {self.surname = }, {self.birthday = }, {self.city = }, {self.bio = })'


class UserImage(BaseCommon):
    __tablename__ = "user_images"

    path = Column(Text)

    user_id = Column(BigInteger, ForeignKey('users.id'))
