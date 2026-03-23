from pydantic import BaseModel, Field


class PostCreateSchema(BaseModel):
    post_text: str = Field(min_length=1, max_length=10000)


class PostUpdateSchema(BaseModel):
    post_text: str = Field(min_length=1, max_length=10000)


class PostInfoSchema(BaseModel):
    id: int
    post_text: str
    owner_id: int
    img_url: str | None = None
