from sqlalchemy import create_engine

from config import config
from db.models import BaseCommon


def create():
    engine = create_engine(f"sqlite:///{config.db.database}.sqlite")
    BaseCommon.metadata.create_all(engine)
