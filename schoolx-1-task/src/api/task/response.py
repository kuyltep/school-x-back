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
  version: int
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)
