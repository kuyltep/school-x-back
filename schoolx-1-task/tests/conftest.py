import sys
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
  sys.path.insert(0, str(PROJECT_ROOT))

from src.api.auth.dependencies import get_current_user
from src.app.app import create_app
from src.database.database import Base
from src.database.repositories import base as base_repository
from src.database.repositories import comment as comment_repository
from src.database.repositories import task as task_repository
from src.database.repositories import user as user_repository


@pytest_asyncio.fixture
async def test_session_maker(monkeypatch):
  engine = create_async_engine(
    "sqlite+aiosqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
  )
  session_maker = async_sessionmaker(engine, expire_on_commit=False)

  async with engine.begin() as connection:
    await connection.run_sync(Base.metadata.create_all)

  monkeypatch.setattr(base_repository, "async_session_maker", session_maker)
  monkeypatch.setattr(task_repository, "async_session_maker", session_maker)
  monkeypatch.setattr(user_repository, "async_session_maker", session_maker)
  monkeypatch.setattr(comment_repository, "async_session_maker", session_maker)

  try:
    yield session_maker
  finally:
    async with engine.begin() as connection:
      await connection.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def app(test_session_maker):
  app = create_app()
  user_id = uuid4()

  async def override_current_user():
    return SimpleNamespace(id=user_id)

  app.dependency_overrides[get_current_user] = override_current_user
  app.state.test_user_id = user_id

  try:
    yield app
  finally:
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(app):
  transport = ASGITransport(app=app)
  async with AsyncClient(transport=transport, base_url="http://testserver") as async_client:
    yield async_client
