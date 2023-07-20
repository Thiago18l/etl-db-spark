from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os


def get_session() -> AsyncSession:
    DATABASE_URL = os.getenv('DATABASE_URL')
    URL = DATABASE_URL.replace(
        'postgres://',
        'postgresql+asyncpg://',
        1
    )
    async_engine = create_async_engine(URL, echo=True, future=True)
    async_session = sessionmaker(async_engine, class_=AsyncSession)
    return async_session()
