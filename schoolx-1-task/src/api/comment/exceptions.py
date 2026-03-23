from fastapi import HTTPException, status


COMMENT_NOT_FOUND_EXCEPTION = HTTPException(
  status_code=status.HTTP_404_NOT_FOUND,
  detail={
    "error": {
      "code": "COMMENT_NOT_FOUND",
      "message": "Comment not found",
    }
  },
)
