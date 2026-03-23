from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field
from src.database.sql_enums import TaskStatus
from src.api.pagination import PaginationParams


class TaskCreate(BaseModel):
  title: str = Field(min_length=1, max_length=255)
  description: str | None = None
  asset_id: UUID | None = None
  version: int | None = Field(default=None, ge=1, le=255)
  status: TaskStatus | None = None


class TaskUpdate(TaskCreate):
  title: str | None = Field(None, min_length=1, max_length=255)


class TaskPaginationParams(PaginationParams):
  sort_by: Literal["title", "status", "created_at", "updated_at"] = "created_at"
