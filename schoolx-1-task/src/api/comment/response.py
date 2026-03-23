from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CommentResponse(BaseModel):
  id: UUID
  user_id: UUID
  task_id: UUID
  parent_id: UUID | None
  content: str
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)
