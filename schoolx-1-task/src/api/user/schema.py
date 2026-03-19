from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
  username: str = Field(min_length=1, max_length=100)
  email: EmailStr
  password: str = Field(min_length=8)
  birthdate: datetime | None = None

class UserUpdate(BaseModel):
  username: str | None = Field(None, min_length=1, max_length=100)
  email: EmailStr | None = None
  birthdate: datetime | None = None

