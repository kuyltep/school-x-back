from typing import Generic, TypeVar, Literal
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")


class PaginationParams(BaseModel):
  page: int = Field(
    1,
    ge=1,
  )
  size: int = Field(10, ge=1, le=100)
  sort_by: str = "created_at"
  order: Literal["asc", "desc"] = "desc"


class PaginatedResponse(BaseModel, Generic[T]):
  items: list[T]
  total: int
  page: int
  size: int
  pages: int

  model_config = ConfigDict(from_attributes=True)
