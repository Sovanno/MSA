from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Настройки подключения к базе данных
    database_main_url: str = Field(..., alias="DATABASE_MAIN_URL")
    database_users_url: str = Field(..., alias="DATABASE_USERS_URL")

    postgres_user: str | None = None
    postgres_password: str | None = None

    # JWT настройки
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Настройки чтения .env файла
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")



# Создаем экземпляр конфигурации
settings = Settings()
