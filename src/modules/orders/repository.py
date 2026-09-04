import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.modules.orders.models import Order, OrderItem


class OrderRepository:
    """Puerta de entrada para Orders. Ningún router ni servicio debe escribir queries SQLAlchemy fuera de aquí."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_all(self) -> list[Order]:
        return self._db.scalars(select(Order).options(selectinload(Order.items))).all()

    def list_by_user(self, user_id: uuid.UUID) -> list[Order]:
        return self._db.scalars(
            select(Order).where(Order.user_id == user_id).options(selectinload(Order.items))
        ).all()

    def get_by_id(self, order_id: uuid.UUID) -> Order | None:
        return self._db.scalar(
            select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        )

    def add(self, order: Order) -> Order:
        self._db.add(order)
        self._db.flush()
        return order

    def add_item(self, item: OrderItem) -> OrderItem:
        self._db.add(item)
        self._db.flush()
        return item

    # --- Límites de transacción (unit of work mínima) ---

    def commit(self) -> None:
        self._db.commit()

    def rollback(self) -> None:
        self._db.rollback()

    def refresh(self, order: Order) -> None:
        self._db.refresh(order)
