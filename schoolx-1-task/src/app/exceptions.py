from fastapi import HTTPException, status

INVALID_API_KEY_EXCEPTION = HTTPException(
  status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or inactive API Key"
)
