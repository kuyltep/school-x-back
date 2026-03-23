from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base

if TYPE_CHECKING:
  from .user import User
  from .task import Task


class Comment(Base):
  user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
  task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), index=True)
  content: Mapped[str] = mapped_column(nullable=False)

  parent_id: Mapped[UUID | None] = mapped_column(
    ForeignKey("comments.id"), nullable=True
  )
  parent: Mapped["Comment | None"] = relationship(
    "Comment", remote_side="Comment.id", back_populates="replies"
  )
  replies: Mapped[list["Comment"]] = relationship(
    "Comment", back_populates="parent", cascade="all, delete-orphan"
  )

  user: Mapped["User"] = relationship("User", back_populates="comments")
  task: Mapped["Task"] = relationship("Task", back_populates="comments")
