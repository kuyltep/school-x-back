from typing import Any, Literal
from uuid import UUID

from sqlalchemy import select

from src.database.database import async_session_maker
from src.database.models.comment import Comment
from src.database.repositories.base import BaseRepository


class CommentRepository(BaseRepository):
  model = Comment

  @classmethod
  async def get_by_task_id(
    cls,
    task_id: UUID,
    parent_id: UUID | None = None,
    page: int = 1,
    size: int = 10,
    sort_by: str = "created_at",
    order: Literal["asc", "desc"] = "desc",
  ) -> tuple[list[Any], int]:
    async with async_session_maker() as session:
      query = select(cls.model).where(cls.model.task_id == task_id)
      if parent_id is None:
        query = query.where(cls.model.parent_id.is_(None))
      else:
        query = query.where(cls.model.parent_id == parent_id)

      total = await cls._get_total_count(session, query)

      query = cls._apply_sorting(query, sort_by, order)
      query = query.offset((page - 1) * size).limit(size)

      result = await session.execute(query)
      items = result.scalars().all()
      return items, total
