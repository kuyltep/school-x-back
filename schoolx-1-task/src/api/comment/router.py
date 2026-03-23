from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.api.auth.dependencies import get_current_user
from src.api.comment.exceptions import COMMENT_NOT_FOUND_EXCEPTION
from src.api.comment.response import CommentResponse
from src.api.comment.schema import CommentCreate, CommentPaginationParams
from src.api.comment.service import CommentService
from src.api.pagination import PaginatedResponse
from src.api.task.exceptions import TASK_NOT_FOUND_EXCEPTION
from src.api.task.service import TaskService
from src.database.models.user import User

router = APIRouter(prefix="/tasks/{task_id}/comments", tags=["Comments"])


@router.get("")
async def get_comments(
  task_id: UUID,
  pagination: Annotated[CommentPaginationParams, Query()],
) -> PaginatedResponse[CommentResponse]:
  task = await TaskService.get_task(str(task_id))
  if not task:
    raise TASK_NOT_FOUND_EXCEPTION
  return await CommentService.get_comments(task_id, pagination)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_comment(
  task_id: UUID,
  data: CommentCreate,
  current_user: User = Depends(get_current_user),
) -> CommentResponse:
  task = await TaskService.get_task(str(task_id))
  if not task:
    raise TASK_NOT_FOUND_EXCEPTION

  if data.parent_id is not None:
    parent = await CommentService.get_comment(str(data.parent_id))
    if not parent or parent.task_id != task_id:
      raise COMMENT_NOT_FOUND_EXCEPTION

  return await CommentService.create_comment(task_id, current_user.id, data)
