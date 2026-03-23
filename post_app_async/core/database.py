from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from core.config import DB_URL

Base = declarative_base()
engine = create_async_engine(DB_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция, которая создает подключение к БД. Используем как зависимость
@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
      try:
          yield db
      finally:
          await db.close()
