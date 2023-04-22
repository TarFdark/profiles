import logging

from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

from db import create_db
from db.models import Base


logger = logging.getLogger(__name__)


async def create_pool(database, echo):
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{database}.sqlite",
        echo=echo,
        future=True,
        poolclass=NullPool,
    )

    if not Path(f"{database}.sqlite").exists():
        create_db.create()
        logger.info("db created")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionmaker
