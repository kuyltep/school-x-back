from fastapi import Response

from src.api.user.response import UserResponse
from src.api.user.schema import UserCreate
from src.database.models.user import User
from src.database.repositories.user import UserRepository

from .dependencies import clear_access_cookie, set_access_cookie
from .exceptions import (
  EMAIL_ALREADY_REGISTERED_EXCEPTION,
  INCORRECT_USERNAME_OR_PASSWORD_EXCEPTION,
  USERNAME_ALREADY_TAKEN_EXCEPTION,
)
from .schema import LoginRequest, MessageResponse, TokenResponse
from .security import create_access_token, get_password_hash, verify_password


class AuthService:
  @staticmethod
  async def register(data: UserCreate, response: Response) -> UserResponse:
    existing_user = await UserRepository.get_by_email(data.email)
    if existing_user:
      raise EMAIL_ALREADY_REGISTERED_EXCEPTION

    existing_username = await UserRepository.get_by_username(data.username)
    if existing_username:
      raise USERNAME_ALREADY_TAKEN_EXCEPTION

    user_data = data.model_dump()
    user_data["password_hash"] = get_password_hash(user_data.pop("password"))
    user = await UserRepository.create(**user_data)

    access_token = create_access_token(data={"sub": str(user.id)})
    set_access_cookie(response, access_token)
    return UserResponse.model_validate(user)

  @staticmethod
  async def login(
    response: Response,
    data: LoginRequest,
  ) -> TokenResponse:
    user = None

    if "@" in data.email_or_username:
      user = await UserRepository.get_by_email(data.email_or_username)

    if not user:
      user = await UserRepository.get_by_username(data.email_or_username)

    if not user or not verify_password(data.password, user.password_hash):
      raise INCORRECT_USERNAME_OR_PASSWORD_EXCEPTION

    access_token = create_access_token(data={"sub": str(user.id)})
    set_access_cookie(response, access_token)
    return TokenResponse(access_token=access_token)

  @staticmethod
  def refresh(response: Response, user: User) -> TokenResponse:
    access_token = create_access_token(data={"sub": str(user.id)})
    set_access_cookie(response, access_token)
    return TokenResponse(access_token=access_token)

  @staticmethod
  def logout(response: Response) -> MessageResponse:
    clear_access_cookie(response)
    return MessageResponse(detail="Logged out successfully")

  @staticmethod
  def me(user: User) -> UserResponse:
    return UserResponse.model_validate(user)