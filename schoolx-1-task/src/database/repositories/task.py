from src.database.repositories.base import BaseRepository
from src.database.models.task import Task
from src.database.sql_enums import TaskStatus


class TaskRepository(BaseRepository):
  model = Task
