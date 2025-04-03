"""Service settings file."""

import typing
import zoneinfo
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    dsn: str = "postgresql+psycopg://postgres:postgres@localhost:5500/delivery-db"
    pool_min_size: int = 5
    pool_max_overflow_size: int = 10
    connection_tries: int = 5
    pool_pre_ping: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    # App settings
    app_host: str = "0.0.0.0"  # noqa: S104
    app_port: int = 8010
    log_level: str = "DEBUG"
    workdir: Path = Path.cwd()
    timezone: str = "Europe/Moscow"

    # Http settings
    http_request_tries_cnt: int = 3

    # Database settings
    database: DBSettings = DBSettings()


settings: typing.Final = Settings()
timezone: typing.Final = zoneinfo.ZoneInfo(settings.timezone)
