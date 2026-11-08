from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    secret_key: SecretStr

    database_url: PostgresDsn

    algorithm: str = "HS256"

    access_token_expire_minutes: int | None = Field(default=30, gt=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )


settings = AppSettings()


# Q1 — Settings from environment variables.
#
# Expose a module-level object named `settings` with these attributes:
#   settings.secret_key                  (str, required)
#   settings.database_url                (str, required)
#   settings.algorithm                   (str, default "HS256")
#   settings.access_token_expire_minutes (int, default 30)
#
# See ASSESSMENT.md for the full requirements.
