from fastapi import APIRouter, status, Depends, Query
from typing import Annotated

from src.api.pagination import PaginatedResponse
from src.database.models.user import User
from src.api.auth.dependencies import get_current_user
from .schema import TaskCreate, TaskUpdate, TaskPaginationParams
from .response import TaskResponse
from .service import TaskService
from .exceptions import TASK_NOT_FOUND_EXCEPTION

router = APIRouter(
  prefix="/tasks", tags=["Tasks"]
)


@router.get("")
async def get_tasks(
  pagination: Annotated[TaskPaginationParams, Query()],
) -> PaginatedResponse[TaskResponse]:
  return await TaskService.get_tasks(pagination)


@router.get("/me")
async def get_my_tasks(
  pagination: Annotated[TaskPaginationParams, Query()],
  current_user: User = Depends(get_current_user),
) -> PaginatedResponse[TaskResponse]:
  return await TaskService.get_my_tasks(current_user.id, pagination)


@router.get("/{id}")
async def get_task(id: str) -> TaskResponse:
  task = await TaskService.get_task(id)
  if not task:
    raise TASK_NOT_FOUND_EXCEPTION
  return task


@router.post("")
async def create_task(
  data: TaskCreate,
  current_user: User = Depends(get_current_user),
) -> TaskResponse:
  return await TaskService.create_task(data, current_user.id)


@router.patch("/{id}")
async def update_task(id: str, data: TaskUpdate) -> TaskResponse:
  task = await TaskService.update_task(id, data)
  if not task:
    raise TASK_NOT_FOUND_EXCEPTION
  return task


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: str):
  success = await TaskService.delete_task(id)
  if not success:
    raise TASK_NOT_FOUND_EXCEPTION
