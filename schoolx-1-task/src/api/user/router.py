from fastapi import APIRouter, status

from .schema import UserCreate, UserUpdate
from .response import UserResponse
from .service import UserService
from .exceptions import USER_NOT_FOUND_EXCEPTION

router = APIRouter(
  prefix="/users", tags=["Users"]
)

@router.get("/{id}")
async def get_user(id: str) -> UserResponse:
  user = await UserService.get_user(id)
  if not user:
    raise USER_NOT_FOUND_EXCEPTION
  return user

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate) -> UserResponse:
  return await UserService.create_user(data)

@router.patch("/{id}")
async def update_user(id: str, data: UserUpdate) -> UserResponse:
  user = await UserService.update_user(id, data)
  if not user:
    raise USER_NOT_FOUND_EXCEPTION
  return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
  success = await UserService.delete_user(id)
  if not success:
    raise USER_NOT_FOUND_EXCEPTION
