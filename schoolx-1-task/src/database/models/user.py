from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import  Mapped, mapped_column, relationship
from src.database.database import Base

if TYPE_CHECKING:
  from .task import Task
  from .comment import Comment


class User(Base):
  username: Mapped[str] = mapped_column(index=True, nullable=False)
  email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
  password_hash: Mapped[str] = mapped_column(nullable=False)
  birthdate: Mapped[datetime] = mapped_column(nullable=True)

  tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")
  comments: Mapped[list["Comment"]] = relationship(
    "Comment", back_populates="user", cascade="all, delete-orphan"
  )