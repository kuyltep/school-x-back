from sqlalchemy import select
from src.database.database import async_session_maker
from src.database.repositories.base import BaseRepository
from src.database.models.user import User


class UserRepository(BaseRepository):
  model = User

  @classmethod
  async def get_by_username(cls, username: str):
    async with async_session_maker() as session:
      query = select(cls.model).filter_by(username=username)
      result = await session.execute(query)
      return result.scalar_one_or_none()

  @classmethod
  async def get_by_email(cls, email: str):
    async with async_session_maker() as session:
      query = select(cls.model).filter_by(email=email)
      result = await session.execute(query)
      return result.scalar_one_or_none()
