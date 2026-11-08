from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    secret_key: SecretStr

    database_url: str

    algorithm: str = "HS256"

    access_token_expire_minutes: int | None = Field(default=30, gt=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )


settings = AppSettings()
