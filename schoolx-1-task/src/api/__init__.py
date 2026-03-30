from fastapi import APIRouter, Depends

from src.api.auth.dependencies import get_current_user
from src.api.auth.router import router as auth_router
from src.api.comment.router import router as comment_router
from src.api.task.router import router as task_router
from src.api.user.router import router as user_router
from src.app.config import configs

router = APIRouter(prefix=configs.api_prefix)

router.include_router(auth_router)
router.include_router(task_router, dependencies=[Depends(get_current_user)])
router.include_router(comment_router, dependencies=[Depends(get_current_user)])
router.include_router(user_router, dependencies=[Depends(get_current_user)])
