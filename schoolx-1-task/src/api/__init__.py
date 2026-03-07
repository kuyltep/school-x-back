from fastapi import APIRouter
from .task.router import router as task_router

router = APIRouter(prefix="/api")

router.include_router(task_router)
