from fastapi import APIRouter, Depends, Response, status

from src.api.user.response import UserResponse
from src.api.user.schema import UserCreate

from .dependencies import get_current_user
from .schema import LoginRequest, MessageResponse, TokenResponse
from .service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
  "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(data: UserCreate, response: Response):
  return await AuthService.register(data, response)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, response: Response):
  return await AuthService.login(response, data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(response: Response, current_user=Depends(get_current_user)):
  return await AuthService.refresh(response, current_user)


@router.post("/logout", response_model=MessageResponse)
async def logout(response: Response):
  return await AuthService.logout(response)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
  return await AuthService.me(current_user)
