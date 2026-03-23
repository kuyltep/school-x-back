from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    limit: int = Field(5, ge=0, le=100)
    offset: int = Field(0, ge=0)

class FilterParams(BaseModel):
    style: str | None = None
    author: str | None = None
