"""Config file."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceSettings(BaseSettings):
    """Servise settings.

    Args:
        BaseSettings (class): Base settings
    """

    model_config = (SettingsConfigDict(
        env_file='.env',
        extra='ignore',
    ))


class PgSqlSettings(ServiceSettings):
    """Settings for PgSql.

    Args:
        ServiseSettings (class): Servise settings
    """

    db_host: str
    db_password: str
    db_port: int
    db_name: str
    db_user: str
    db_driver: str
    db_shema: str


class JwtSettings(ServiceSettings):
    """Settings for JWT.

    Args:
        ServiceSettings (class): Servise settings
    """

    JWT_SEKRET_KEY: str
    ALGORITM: str
    ACCESS_TIME: int
    REFRESH_TIME: int


jwtsettings = JwtSettings()
pgsqlsettings = PgSqlSettings()
