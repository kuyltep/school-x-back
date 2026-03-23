from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from src.api.pagination import PaginationParams


class CommentCreate(BaseModel):
  content: str = Field(min_length=1, max_length=2000)
  parent_id: UUID | None = None


class CommentPaginationParams(PaginationParams):
  parent_id: UUID | None = None
  sort_by: Literal["created_at", "updated_at"] = "created_at"
