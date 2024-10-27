from dataclasses import dataclass
from enum import Enum

import bcrypt
from pydantic import BaseModel, EmailStr, Field


class UserRole(Enum):
    """Класс выбора роли пользователя."""

    USER = 'user'
    ADMIN = 'admin'


@dataclass
class ValidUsers(BaseModel):
    """Валидация данный в таблицу Users."""

    email: EmailStr
    name: str
    surname: str
    role: UserRole.User
    password: Field(min_length=5)

    def hashing_password(self, password):

        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)

        return hash
