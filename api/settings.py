"""Service settings file."""

import typing
import zoneinfo
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    dsn: str = "postgresql+psycopg://username:secret@localhost:5432/delivery"
    pool_min_size: int = 5
    pool_max_overflow_size: int = 10
    connection_tries: int = 5
    pool_pre_ping: bool = True


class JobsSettings(BaseSettings):

    assign_orders_job_id: str = "assign_orders_job"
    assign_orders_run_every_sec: int = 1

    move_couriers_job_id: str = "move_couriers_job"
    move_couriers_run_every_sec: int = 2


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    # App settings
    app_host: str = "0.0.0.0"  # noqa: S104
    app_port: int = 8082
    log_level: str = "DEBUG"
    workdir: Path = Path.cwd()
    timezone: str = "Europe/Moscow"

    # Http settings
    http_request_tries_cnt: int = 3

    # Database settings
    database: DBSettings = DBSettings()

    # Jobs settings
    jobs: JobsSettings = JobsSettings()


settings: typing.Final = Settings()
timezone: typing.Final = zoneinfo.ZoneInfo(settings.timezone)
