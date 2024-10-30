import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID  # Для UUID
from sqlalchemy.orm import (DeclarativeBase, Mapped, declarative_mixin,
                            mapped_column, relationship)


class Base(DeclarativeBase):
    """Default base model."""

    pass


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
        DateTime(timezone=True), server_default=func.now(),
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(),
    )


class Product(UUIDMixin, TimestampMixin):
    """Таблица товаров."""

    __tablename__ = 'product'

    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(1000))
    price: Mapped[Numeric(10, 2)]
    stock: Mapped[int]

    category = relationship('ProductCategory', back_populates='product')


class Category(UUIDMixin, TimestampMixin):
    """Таблица категорий."""

    __tablename__ = 'category'

    category_name: Mapped[str] = mapped_column(
        String(50), nullable=False,
    )
    description: Mapped[str] = mapped_column(String(1000))

    products = relationship('ProductCategory', back_populates='category')


class ProductCategory(UUIDMixin, TimestampMixin):
    """Таблица связующая Product и Category."""

    __tablename__ = 'product_category'

    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('product.id'),
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('category.id'), default=uuid.uuid4,
    )

    product = relationship('Product', back_populates='category')
    category = relationship('Category', back_populates='product')


class Customer(UUIDMixin, TimestampMixin):
    """Таблица данных о покупателк."""

    __tablename__ = 'customer'

    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str] = mapped_column(String, unique=True)
    phone: Mapped[str]
    address: Mapped[str]  # Поментять str на словарь

    order = relationship('Order', back_populates='customer')
    cart = relationship('Cart', back_populates='customer')


class OrderStatus(Enum):
    """Возможные статусы заказа."""

    PENDING = 'pending'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


class Order(UUIDMixin, TimestampMixin):
    """Таблица заказа."""

    __tablename__ = 'order'

    customer_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('customer.id'), default=uuid.uuid4,
    )

    order_date: Mapped[datetime] = mapped_column(
        DateTime(timezone), server_default=func.now(), onupdate=func.now(),
    )

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING,
    )

    total_amount: Mapped[Numeric(10, 2)]

    customer = relationship('Customer', back_populates='order')
    items = relationship('OrderItem', back_populates='order')


class OrderItem(UUIDMixin, TimestampMixin):
    """Товары в звказе."""

    __tablename__ = 'order_item'

    order_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('order.id'), default=uuid.uuid4,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('product.id'), default=uuid.uuid4,
    )

    quantity: Mapped[int]  # Кол-во вещей в заказе

    price: Mapped[Numeric]

    order = relationship('Order', back_populates='items')
    product = relationship('Product')


class StatusPay(Enum):
    """Возможные статусы оплаты."""

    COMPLETED = 'completed'
    FAILED = 'failed'
    EXPECTATION = 'waiting for payment'


class Payment(UUIDMixin, TimestampMixin):
    """Схема платежей."""

    __tablename__ = 'payment'

    order_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('order.id'), default=uuid.uuid4,
    )

    amount: Mapped[Numeric(10, 2)]

    payment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
    )

    status: Mapped[StatusPay] = mapped_column(
        Enum(StatusPay), nullable=False, default=StatusPay.EXPECTATION,

    )

    order = relationship('Order', back_populates='payment')


class Cart(TimestampMixin, UUIDMixin):
    """Корзина."""

    __tablename__ = 'cart'

    customer_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('customer.id'), default=uuid.uuid4,
    )

    customer = relationship('Customer', back_populates='cart')

    cart_item = relationship('CartItem', back_populates='cart')


class CartItem(UUIDMixin, TimestampMixin):
    """Товары в корзине."""

    __tablename__ = 'cart_item'

    cart_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('cart.id'), default=uuid.uuid4,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey('product.id'), default=uuid.uuid4,
    )

    quantity: Mapped[int]  # Кол-во продуктов

    product = relationship('Product')
    cart = relationship('Cart', back_populates='cart_item')
