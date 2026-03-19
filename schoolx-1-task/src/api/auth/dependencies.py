from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param

from src.database.models.user import User
from src.database.repositories.user import UserRepository

from .security import (
    ACCESS_TOKEN_COOKIE_KEY,
    ACCESS_TOKEN_COOKIE_MAX_AGE,
    TokenDecodeError,
    decode_access_token,
)


def set_access_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_KEY,
        value=token,
        httponly=True,
        max_age=ACCESS_TOKEN_COOKIE_MAX_AGE,
        samesite="lax",
        secure=False,
    )


def clear_access_cookie(response: Response) -> None:
    response.delete_cookie(key=ACCESS_TOKEN_COOKIE_KEY)


class HTTPBearerCookie(HTTPBearer):
    async def __call__(self, request: Request) -> str | None:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)

        if authorization and scheme.lower() == "bearer":
            return credentials

        token = request.cookies.get(ACCESS_TOKEN_COOKIE_KEY)
        if token:
            return token

        if self.auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        return None


auth_scheme = HTTPBearerCookie(
    auto_error=True,
    bearerFormat="JWT",
    scheme_name="BearerAuth",
)


async def get_current_user(
    token: str = Depends(auth_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except TokenDecodeError:
        raise credentials_exception

    user = await UserRepository.get_by_id(user_id)
    if not user:
        raise credentials_exception
    return user
