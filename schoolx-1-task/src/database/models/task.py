from typing import TYPE_CHECKING

from uuid import UUID

from src.database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from ..sql_enums import TaskStatus

if TYPE_CHECKING:
  from .user import User
  from .comment import Comment


class Task(Base):
  title: Mapped[str]
  status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.PENDING)
  description: Mapped[str | None]
  asset_id: Mapped[UUID | None] = mapped_column(Uuid, index=True)
  version: Mapped[int] = mapped_column(default=1)
  user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)

  user: Mapped["User"] = relationship("User", back_populates="tasks")
  comments: Mapped[list["Comment"]] = relationship(
    "Comment", back_populates="task", cascade="all, delete-orphan"
  )
