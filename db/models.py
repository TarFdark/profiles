from sqlalchemy import Column, BigInteger, Text

from db.base import Base


class BaseCommon(Base):
    __tablename__ = "common"

    field1 = Column(BigInteger, primary_key=True)
    field2 = Column(Text, default="default_value")
