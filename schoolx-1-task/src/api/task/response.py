from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from src.database.sql_enums import TaskStatus


class TaskResponse(BaseModel):
  id: UUID
  title: str
  status: TaskStatus
  description: str | None
  asset_id: UUID | None
  avatar_url: str | None
  version: int
  created_at: datetime
  updated_at: datetime
  user_id: UUID

  model_config = ConfigDict(from_attributes=True)


class TaskAvatarUploadResponse(BaseModel):
  url: str
  task_id: UUID
  bucket: str
  object_key: str
