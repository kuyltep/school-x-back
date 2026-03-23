from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator

class UserCreate(BaseModel):
  username: str = Field(min_length=1, max_length=100)
  email: EmailStr
  password: str = Field(min_length=8)
  birthdate: datetime | None = None

  @field_validator('birthdate')
  @classmethod
  def remove_timezone(cls, v: datetime | None) -> datetime | None:
    if v is not None and v.tzinfo is not None:
        return v.replace(tzinfo=None)
    return v

class UserUpdate(BaseModel):
  username: str | None = Field(None, min_length=1, max_length=100)
  email: EmailStr | None = None
  birthdate: datetime | None = None

  @field_validator('birthdate')
  @classmethod
  def remove_timezone(cls, v: datetime | None) -> datetime | None:
    if v is not None and v.tzinfo is not None:
        return v.replace(tzinfo=None)
    return v

