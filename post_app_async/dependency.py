from typing import Annotated, Any
from fastapi import Depends, HTTPException
from fastapi.requests import Request
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import decode_access_token
from models import User
from repositories import UserRepository

from schemas.dependency import PaginationParams, FilterParams

PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]
FilterParamsDep = Annotated[FilterParams, Depends(FilterParams)]


async def get_current_user(request: Request, repository: UserRepository = Depends(UserRepository)) -> Any:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Отсутствует токен")

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Невалидный токен")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Невалидный токен")

    user = await repository.get_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]