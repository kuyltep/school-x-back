from pydantic import BaseModel


class LoginRequest(BaseModel):
  email_or_username: str
  password: str


class TokenResponse(BaseModel):
  access_token: str
  token_type: str = "bearer"


class MessageResponse(BaseModel):
  detail: str
