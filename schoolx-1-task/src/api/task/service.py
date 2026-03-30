import math
from uuid import UUID

from fastapi import HTTPException, UploadFile, status

from src.api.pagination import PaginatedResponse
from src.api.task.response import TaskAvatarUploadResponse, TaskResponse
from src.api.task.schema import TaskCreate, TaskPaginationParams, TaskUpdate
from src.app.config import configs
from src.app.services.minio import MinioServiceError, MinioStorageService
from src.database.repositories.task import TaskRepository


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
    pagination: TaskPaginationParams,
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

  @staticmethod
  async def upload_avatar(id: str, file: UploadFile) -> TaskAvatarUploadResponse | None:
    task = await TaskRepository.get_by_id(id)
    if not task:
      return None

    content_type = file.content_type or ""
    if not content_type.startswith(configs.avatar_allowed_mime_prefix):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Only image/* files are allowed",
      )

    content = await file.read(configs.avatar_max_bytes + 1)
    if not content:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Uploaded file is empty",
      )

    if len(content) > configs.avatar_max_bytes:
      raise HTTPException(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        detail=f"File is too large. Max size is {configs.avatar_max_bytes} bytes",
      )

    storage = MinioStorageService.from_settings(configs)
    try:
      uploaded = await storage.upload_avatar(
        task_id=task.id,
        filename=file.filename,
        content=content,
        content_type=content_type,
      )
    except MinioServiceError as exc:
      raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=str(exc),
      ) from exc

    updated = await TaskRepository.update_by_id(id, avatar_url=uploaded.url)
    if not updated:
      return None

    return TaskAvatarUploadResponse(
      url=uploaded.url,
      task_id=updated.id,
      bucket=uploaded.bucket,
      object_key=uploaded.object_key,
    )
