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
