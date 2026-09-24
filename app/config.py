from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"  # игнорировать переменные в .env, которых нет в классе
    )
    
    # Telegram
    telegram_api_id: int = 0
    telegram_api_hash: str = ""
    telegram_bot_token: str = ""
    telegram_session_name: str = "monitor_session"

    # БД
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379

    @property
    def database_url(self) -> URL:
        return URL.create(
            "postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )
        





@lru_cache
def get_settings() -> Settings:
    return Settings()

    
