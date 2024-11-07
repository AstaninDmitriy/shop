"""Файл по работе с JWT."""
from datetime import datetime, timedelta

from config.config import jwtsettings
from jose import jwt


class JwtTokens():
    """Класс по работе с jwt."""

    def __init__(self):
        """Init func."""
        self.algorim = jwtsettings.ALGORITM
        self.accesstime = jwtsettings.ACCESS_TIME
        self.refreshtime = jwtsettings.REFRESH_TIME
        self.sekretkey = jwtsettings.JWT_SEKRET_KEY

    def create_access_tokens(self, id: int) -> str:
        """Создайние access token.

        Args:
            id (int): id пользователя

        Returns:
            str: access token 
        """
        exp = datetime.now() + timedelta(minutes=(self.accesstime))
        jwtdecode = {'exp': exp, 'sub': str(id)}
        return jwt.encode(jwtdecode, self.sekretkey, self.algorim)


jwttokens = JwtTokens()
