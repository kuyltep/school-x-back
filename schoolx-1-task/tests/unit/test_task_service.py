from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.api.task.schema import TaskCreate
from src.api.task.service import TaskService
from src.database.models.task import Task
from src.database.repositories.task import TaskRepository
from src.database.sql_enums import TaskStatus


@pytest.mark.asyncio
async def test_create_task(monkeypatch):
  user_id = uuid4()
  now = datetime.now(UTC)
  task = Task(
    id=uuid4(),
    title="Task from unit test",
    status=TaskStatus.PENDING,
    description="desc",
    asset_id=None,
    version=1,
    user_id=user_id,
    created_at=now,
    updated_at=now,
  )

  create_mock = AsyncMock(return_value=task)
  monkeypatch.setattr(TaskRepository, "create", create_mock)

  data = TaskCreate(title="Task from unit test", description="desc")
  result = await TaskService.create_task(data, user_id)

  create_mock.assert_awaited_once_with(**data.model_dump(), user_id=user_id)
  assert result.id == task.id
  assert result.title == task.title
  assert result.user_id == user_id
