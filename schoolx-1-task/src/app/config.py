from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Configs(BaseSettings):
  port: int = 8000
  origins: list[str] = ["*"]

  db_host: str
  db_port: int
  db_name: SecretStr
  db_user: SecretStr
  db_password: SecretStr
  secret_key: SecretStr

  def get_db_url(self):
    return f"postgresql+asyncpg://{self.db_user.get_secret_value()}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name.get_secret_value()}"

  model_config = SettingsConfigDict(extra="forbid", env_file=".env")


configs = Configs()
