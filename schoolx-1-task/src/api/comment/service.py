import math
from uuid import UUID

from src.api.comment.response import CommentResponse
from src.api.comment.schema import CommentCreate, CommentPaginationParams
from src.api.pagination import PaginatedResponse
from src.database.repositories.comment import CommentRepository


class CommentService:
  @staticmethod
  async def create_comment(
    task_id: UUID,
    user_id: UUID,
    data: CommentCreate,
  ) -> CommentResponse:
    comment = await CommentRepository.create(
      task_id=task_id,
      user_id=user_id,
      **data.model_dump(),
    )
    return CommentResponse.model_validate(comment)

  @staticmethod
  async def get_comment(id: str) -> CommentResponse | None:
    comment = await CommentRepository.get_by_id(id)
    if not comment:
      return None
    return CommentResponse.model_validate(comment)

  @staticmethod
  async def get_comments(
    task_id: UUID,
    pagination: CommentPaginationParams,
  ) -> PaginatedResponse[CommentResponse]:
    items, total = await CommentRepository.get_by_task_id(
      task_id=task_id,
      parent_id=pagination.parent_id,
      page=pagination.page,
      size=pagination.size,
      sort_by=pagination.sort_by,
      order=pagination.order,
    )

    pages = math.ceil(total / pagination.size) if total > 0 else 0

    return PaginatedResponse(
      items=[CommentResponse.model_validate(item) for item in items],
      total=total,
      page=pagination.page,
      size=pagination.size,
      pages=pages,
    )
