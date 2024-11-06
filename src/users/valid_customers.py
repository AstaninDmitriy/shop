from typing import List

from pydantic import BaseModel, EmailStr, Field, field_validator


class Address(BaseModel): # noqa
    street: str = Field(..., min_length=4, examples=['Komsomolskaya'])
    house: int = Field(..., examples=[5])
    floor: int = Field(..., examples=[4])
    flat: int = Field(..., examples=[3])


class Customer(BaseModel): # noqa
    name: str = Field(
        min_length=2,
        max_length=12,
        description='Имя пользователя',
        examples=['Ivan'],
    )
    surname: str = Field(
        min_length=2,
        max_length=24,
        description='Фамилия пользователя',
        examples=['Ivanov'],
    )
    email: EmailStr
    phone: str = Field(examples=['+7123456789'])
    address: List[Address]

    @classmethod
    @field_validator('name', 'surname')
    def validate_name(cls, value):
        if not value.isalpha():
            raise ValueError('Имя и фамилия должны содержать только буквы')
        return value.title()
