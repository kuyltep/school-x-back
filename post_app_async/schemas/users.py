from pydantic import BaseModel, EmailStr, Field


class UserRegistrationSchema(BaseModel):
    username: str = Field(min_length=4, max_length=32)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class UserInfoSchema(BaseModel):
    id: int
    username: str
    email: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


class AccessTokenSchema(BaseModel):
    access_token: str
    token_type: str

