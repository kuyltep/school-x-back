from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
  port: int = 8000
  api_prefix: str = "/v1"
  app_env: str = "dev"
  app_version: str = "0.1.0"
  origins: list[str] = ["*"]

  db_host: str
  db_port: int
  db_name: SecretStr
  db_user: SecretStr
  db_password: SecretStr
  secret_key: SecretStr

  minio_endpoint: str = "http://minio:9000"
  minio_access_key: SecretStr = SecretStr("minioadmin")
  minio_secret_key: SecretStr = SecretStr("minioadmin")
  minio_bucket: str = "task-avatars"
  minio_secure: bool = False
  minio_public_url: str = "http://localhost:9000"

  avatar_max_bytes: int = 15 * 1024 * 1024
  avatar_allowed_mime_prefix: str = "image/"

  def get_db_url(self) -> str:
    return (
      f"postgresql+asyncpg://{self.db_user.get_secret_value()}:"
      f"{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/"
      f"{self.db_name.get_secret_value()}"
    )

  model_config = SettingsConfigDict(extra="forbid", env_file=".env")


configs = Configs()
