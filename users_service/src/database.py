from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings
from typing import AsyncGenerator

DATABASE_URL = settings.database_users_url  # например: "postgresql+asyncpg://user:pass@host:port/dbname"

# Асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# Асинхронная сессия
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Базовый класс моделей
base = declarative_base()

# Dependency для FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
