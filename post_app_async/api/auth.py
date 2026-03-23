from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.requests import Request

from schemas import UserRegistrationSchema
from schemas.users import UserInfoSchema, UserLoginSchema, AccessTokenSchema
from services import UserService
from core.security import decode_access_token


router = APIRouter(prefix= "/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
        user: UserRegistrationSchema,
        service: UserService = Depends()
) -> UserInfoSchema:
    db_user = await service.create_user(user)

    return db_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
        response: Response,
        credentials: UserLoginSchema,
        service: UserService = Depends()
) -> AccessTokenSchema:
    token = await service.authenticate_user(credentials)
    response.set_cookie(key="access_token", value=token.access_token, httponly=True)

    return token


@router.get("/test")
def test_auth(
        request: Request,
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    token_details = decode_access_token(token)



    return JSONResponse({"username": token_details.get("sub")})