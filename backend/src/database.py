from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import settings

DATABASE_URL = settings.database_main_url

# Асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True, future=True, pool_pre_ping=True)

# Асинхронный sessionmaker
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Базовый класс для моделей
base = declarative_base()

# Зависимость FastAPI для получения асинхронной сессии
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
