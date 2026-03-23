from pydantic_settings import BaseSettings, SettingsConfigDict

# Класс настроек, в котором описываем структуру конфигурации.
class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_user: str
    db_pass: str
    db_name: str

    secret_key: str

    s3_bucket: str
    s3_url: str
    s3_access_key: str
    s3_secret_key: str
    s3_region: str

    # Конфигурация источника данных (в данном случае .env)
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

# Собираем URL для подключения к БД
DB_URL = f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
