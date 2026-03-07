from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr

from uuid import uuid4, UUID
from src.app.config import configs


DATABASE_URL = configs.get_db_url()

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
  __abstract__ = True

  id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
  created_at: Mapped[datetime] = mapped_column(server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(
    server_default=func.now(), onupdate=func.now()
  )

  @declared_attr.directive
  def __tablename__(cls) -> str:
    return cls.__name__.lower() + "s"


async def get_async_session():
  async with async_session_maker() as session:
    yield session
