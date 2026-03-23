import pytest
from uuid import UUID

from src.database.repositories.task import TaskRepository


@pytest.mark.asyncio
async def test_create_task(client, app):
  payload = {
    "title": "Task from integration test",
    "description": "created by endpoint",
  }

  response = await client.post("/api/tasks", json=payload)

  assert response.status_code == 201
  body = response.json()
  assert body["title"] == payload["title"]
  assert body["description"] == payload["description"]
  assert body["user_id"] == str(app.state.test_user_id)

  stored_task = await TaskRepository.get_by_id(UUID(body["id"]))
  assert stored_task is not None
  assert stored_task.title == payload["title"]
