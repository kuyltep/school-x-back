import math
from uuid import UUID

from src.database.repositories.task import TaskRepository
from src.api.task.schema import TaskCreate, TaskUpdate, TaskPaginationParams
from src.api.task.response import TaskResponse
from src.api.pagination import PaginatedResponse


class TaskService:
  @staticmethod
  async def create_task(data: TaskCreate, user_id: UUID) -> TaskResponse:
    task = await TaskRepository.create(**data.model_dump(), user_id=user_id)
    return TaskResponse.model_validate(task)

  @staticmethod
  async def get_task(id: str) -> TaskResponse | None:
    task = await TaskRepository.get_by_id(id)
    if not task:
      return None
    return TaskResponse.model_validate(task)

  @staticmethod
  async def update_task(id: str, data: TaskUpdate) -> TaskResponse | None:
    update_data = data.model_dump(exclude_unset=True)
    task = await TaskRepository.update_by_id(id, **update_data)
    if not task:
      return None
    return TaskResponse.model_validate(task)

  @staticmethod
  async def delete_task(id: str) -> bool:
    return await TaskRepository.delete_by_id(id)

  @staticmethod
  async def get_tasks(
    pagination: TaskPaginationParams
  ) -> PaginatedResponse[TaskResponse]:
    items, total = await TaskRepository.get_by_filters(
      page=pagination.page,
      size=pagination.size,
      sort_by=pagination.sort_by,
      order=pagination.order,
    )

    pages = math.ceil(total / pagination.size) if total > 0 else 0

    return PaginatedResponse(
      items=[TaskResponse.model_validate(item) for item in items],
      total=total,
      page=pagination.page,
      size=pagination.size,
      pages=pages,
    )

  @staticmethod
  async def get_my_tasks(
    user_id: UUID,
    pagination: TaskPaginationParams,
  ) -> PaginatedResponse[TaskResponse]:
    items, total = await TaskRepository.get_by_user_id(
      user_id=user_id,
      page=pagination.page,
      size=pagination.size,
      sort_by=pagination.sort_by,
      order=pagination.order,
    )

    pages = math.ceil(total / pagination.size) if total > 0 else 0

    return PaginatedResponse(
      items=[TaskResponse.model_validate(item) for item in items],
      total=total,
      page=pagination.page,
      size=pagination.size,
      pages=pages,
    )
