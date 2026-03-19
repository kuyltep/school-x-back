from src.database.repositories.user import UserRepository
from src.api.user.schema import UserCreate, UserUpdate
from src.api.user.response import UserResponse
from src.api.auth.security import get_password_hash

class UserService:
  @staticmethod
  async def create_user(data: UserCreate) -> UserResponse:
    user_data = data.model_dump()
    password = user_data.pop("password")
    user_data["password_hash"] = get_password_hash(password)
    
    user = await UserRepository.create(**user_data)
    return UserResponse.model_validate(user)

  @staticmethod
  async def get_user(id: str) -> UserResponse | None:
    user = await UserRepository.get_by_id(id)
    if not user:
      return None
    return UserResponse.model_validate(user)

  @staticmethod
  async def update_user(id: str, data: UserUpdate) -> UserResponse | None:
    update_data = data.model_dump(exclude_unset=True)
    user = await UserRepository.update_by_id(id, **update_data)
    if not user:
      return None
    return UserResponse.model_validate(user)

  @staticmethod
  async def delete_user(id: str) -> bool:
    return await UserRepository.delete_by_id(id)