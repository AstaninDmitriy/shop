"""Файл для работы с базами данных."""
from config.config import pgsqlsettings


class PostgreSql():
    def __init__(self):
        self.DSN = '{driver}://{name}:{password}@{host}/{port}:{user}'.format(
            driver=pgsqlsettings.db_driver,
            name=pgsqlsettings.db_name,
            password=pgsqlsettings.db_password,
            host=pgsqlsettings.db_host,
            port=pgsqlsettings.db_port,
            user=pgsqlsettings.db_user
        )