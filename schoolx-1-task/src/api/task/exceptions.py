from fastapi import HTTPException, status


TASK_NOT_FOUND_EXCEPTION = HTTPException(
  status_code=status.HTTP_404_NOT_FOUND,
  detail={
    "error": {
      "code": "TASK_NOT_FOUND",
      "message": "Task not found",
    }
  },
)
