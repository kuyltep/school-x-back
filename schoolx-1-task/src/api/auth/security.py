from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from src.app.config import configs

ph = PasswordHasher()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ACCESS_TOKEN_COOKIE_KEY = "access_token"
ACCESS_TOKEN_COOKIE_MAX_AGE = ACCESS_TOKEN_EXPIRE_MINUTES * 60


class TokenDecodeError(Exception):
  pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
  try:
    return ph.verify(hashed_password, plain_password)
  except (VerifyMismatchError, VerificationError, InvalidHashError):
    return False


def get_password_hash(password: str) -> str:
  return ph.hash(password)


def create_access_token(data: dict) -> str:
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  return jwt.encode(
    to_encode,
    configs.secret_key.get_secret_value(),
    algorithm=ALGORITHM,
  )


def decode_access_token(token: str) -> dict:
  try:
    return jwt.decode(
      token,
      configs.secret_key.get_secret_value(),
      algorithms=[ALGORITHM],
    )
  except jwt.PyJWTError as error:
    raise TokenDecodeError from error
