from enum import Enum


class TaskStatus(str, Enum):
  PENDING = "ожидание"
  IN_PROGRESS = "в работе"
  VALIDATION = "валидация"
  DONE = "выполнена"
