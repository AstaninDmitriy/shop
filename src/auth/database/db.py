"""Файл для работы с базами данных."""
from config.config import pgsqlsettings


class PostgreSql():
    """Класс для работы с pgsql."""

    def __init__(self):
        """Init func."""
        self.DSN = '{driver}://{user}:{password}@{host}:{port}/{name}'.format(
            driver=pgsqlsettings.db_driver,
            user=pgsqlsettings.db_user,
            password=pgsqlsettings.db_password,
            host=pgsqlsettings.db_host,
            port=pgsqlsettings.db_port,
            name=pgsqlsettings.db_name,
        )
