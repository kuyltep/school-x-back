from uuid import UUID

from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from ..sql_enums import TaskStatus


class Task(Base):
  title: Mapped[str]
  status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.PENDING)
  description: Mapped[str | None]
  asset_id: Mapped[UUID | None] = mapped_column(Uuid, index=True)
  version: Mapped[int] = mapped_column(default=1)
