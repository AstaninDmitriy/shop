"""Файл для работы с хэшированием."""
import bcrypt


class Hash():
    """Класс по работе с хэшем."""

    def __init__(self):
        """Init func."""
        self.salt = bcrypt.gensalt()

    def create_hash(self, password: str):
        """Хэшированние пароля.

        Args:
            password (str): пароль

        Returns:
            _type_: хэшированный пароль
        """
        return (bcrypt.hashpw(password.encode('utf-8'), self.salt)).decode(
            'utf-8',
        )

    def check_hash(self, password: str, hashed_password: str):
        """Проверка паролей.

        Args:
            password (str): пароль
            hashed_password (str): хэшированный пароль

        Returns:
            bool: провека паролей
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8'),
        )


hast = Hash()
