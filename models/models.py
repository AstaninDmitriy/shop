import uuid
from datetime import datetime
from enum import Enum

import bcrypt
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID  # Для UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (Mapped, declarative_mixin, mapped_column,
                            relationship)

Base = declarative_base()


class UserRole(Enum):
    """Класс выбора роли пользователя."""

    USER = 'user'
    ADMIN = 'admin'


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


@declarative_mixin
class UUIDMixin(Base):
    """Миксин для добавления уникального идентификатора."""

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )


@declarative_mixin
class TimestampMixin(Base):
    """Миксин для добавления временных меток создания и обновления."""

    created_at: Mapped[str] = mapped_column(
        datetime(timezone=True), server_default=func.now(),
    )
    updated_at: Mapped[str] = mapped_column(
        datetime(timezone=True), onupdate=func.now(),
    )


class Product(UUIDMixin, TimestampMixin):
    """Таблица товаров."""

    __tablename__ = 'products'

    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(1000))
    price: Mapped[float]  # Поменять тип данных
    stock: Mapped[int]

    categories = relationship('ProductCategory', back_populates='product')


class Category(UUIDMixin, TimestampMixin):
    """Таблица категорий."""

    __tablename__ = 'categories'

    category_name: Mapped[str] = mapped_column(
        String(50), nullable=False,
    )
    description: Mapped[str] = mapped_column(String(1000))

    products = relationship('ProductCategory', back_populates='category')


class ProductCategory(UUIDMixin, TimestampMixin):
    """Таблица связующая Product и Category."""

    __tablename__ = 'product_category'

    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('products.id'),
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('categories.id'),
    )

    product = relationship('Product', back_populates='categories')
    category = relationship('Category', back_populates='products')
