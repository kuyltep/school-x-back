from fastapi import APIRouter, Depends
from .task.router import router as task_router
from .user.router import router as user_router
from .auth.router import router as auth_router
from .auth.dependencies import get_current_user

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(task_router, dependencies=[Depends(get_current_user)])
router.include_router(user_router, dependencies=[Depends(get_current_user)])
