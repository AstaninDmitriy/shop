"""Config file."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiseSettings(BaseSettings):
    """Servise settings.

    Args:
        BaseSettings (class): Base settings
    """

    model_config = (SettingsConfigDict(
        env_file='.env',
        extra='ignore',
    ))


class PgSqlSettings(ServiseSettings):
    """Settings for PgSql.

    Args:
        ServiseSettings (class): Servise settings
    """

    db_host: str
    db_password: str
    db_port: int
    db_shema: str
    db_name: str
    db_user: str
    db_driver: str


class RedisClient(ServiseSettings):
    """Settings for Redis.

    Args:
        ServiseSettings (class): Servise settings
    """

    redis_host: str
    redis_port: int
    redis_db: int


pgsqlsettings = PgSqlSettings()
