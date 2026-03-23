from fastapi import HTTPException, status


EMAIL_ALREADY_REGISTERED_EXCEPTION = HTTPException(
  status_code=status.HTTP_400_BAD_REQUEST,
  detail="Email already registered",
)

USERNAME_ALREADY_TAKEN_EXCEPTION = HTTPException(
  status_code=status.HTTP_400_BAD_REQUEST,
  detail="Username already taken",
)

INCORRECT_USERNAME_OR_PASSWORD_EXCEPTION = HTTPException(
  status_code=status.HTTP_401_UNAUTHORIZED,
  detail="Incorrect username or password",
)
