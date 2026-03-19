from src.database.repositories.base import BaseRepository
from src.database.models.task import Task
from src.database.database import async_session_maker
from typing import Any, List, Literal, Tuple
from uuid import UUID

from sqlalchemy import select


class TaskRepository(BaseRepository):
  model = Task

  @classmethod
  async def get_by_user_id(
    cls,
    user_id: UUID,
    page: int = 1,
    size: int = 10,
    sort_by: str = "created_at",
    order: Literal["asc", "desc"] = "desc",
  ) -> Tuple[List[Any], int]:
    async with async_session_maker() as session:
      query = select(cls.model).where(cls.model.user_id == user_id)

      total = await cls._get_total_count(session, query)

      query = cls._apply_sorting(query, sort_by, order)
      query = query.offset((page - 1) * size).limit(size)

      result = await session.execute(query)
      items = result.scalars().all()
      return items, total
