from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
  id: UUID
  username: str
  email: str
  birthdate: datetime | None = None
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True, extra="ignore")
