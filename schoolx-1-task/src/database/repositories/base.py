from typing import Any, List, Tuple, Literal
from sqlalchemy import select, update, asc, desc, func, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import async_session_maker


class BaseRepository:
  model = None

  @classmethod
  async def get_by_id(cls, id: str):
    async with async_session_maker() as session:
      query = select(cls.model).filter_by(id=id)
      result = await session.execute(query)
      return result.scalar_one_or_none()

  @classmethod
  async def create(cls, **data):
    async with async_session_maker() as session:
      row = cls.model(**data)
      session.add(row)
      await session.commit()
      await session.refresh(row)
      return row

  @classmethod
  async def update_by_id(cls, id: str, **update_data):
    async with async_session_maker() as session:
      query = (
        update(cls.model)
        .where(cls.model.id == id)
        .values(**update_data)
        .returning(cls.model)
      )
      result = await session.execute(query)
      await session.commit()
      return result.scalar_one_or_none()

  @classmethod
  async def delete_by_id(cls, id: str) -> bool:
    async with async_session_maker() as session:
      row = await session.get(cls.model, id)
      if row:
        await session.delete(row)
        await session.commit()
        return True
      return False

  @classmethod
  async def get_by_filters(
    cls,
    page: int = 1,
    size: int = 10,
    sort_by: str = "created_at",
    order: Literal["asc", "desc"] = "desc",
  ) -> Tuple[List[Any], int]:
    async with async_session_maker() as session:
      query = select(cls.model)

      total = await cls._get_total_count(session, query)

      query = cls._apply_sorting(query, sort_by, order)

      query = query.offset((page - 1) * size).limit(size)

      result = await session.execute(query)
      items = result.scalars().all()
      return items, total

  @classmethod
  async def _get_total_count(cls, session: AsyncSession, query: Select) -> int:

    count_subquery = query.subquery()
    count_query = select(func.count()).select_from(count_subquery)
    total = await session.execute(count_query)
    return total.scalar() or 0

  @classmethod
  def _apply_sorting(cls, query: Select, sort_by: str, order: str) -> Select:
    attr = getattr(cls.model, sort_by, None)
    if attr is not None:
      if order == "asc":
        query = query.order_by(asc(attr))
      else:
        query = query.order_by(desc(attr))
    return query
