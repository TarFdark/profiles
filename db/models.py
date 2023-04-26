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


class UserImage(BaseCommon):
    __tablename__ = "user_images"

    path = Column(Text)

    user_telegram_id = Column(BigInteger, ForeignKey('users.telegram_id'))
