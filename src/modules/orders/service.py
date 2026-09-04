import logging
import uuid

from src.modules.orders.enums import OrderStatus
from src.modules.orders.exceptions import OrderNotFoundError
from src.modules.orders.models import Order, OrderItem
from src.modules.orders.repository import OrderRepository
from src.modules.orders.schemas import OrderCreate
from src.modules.products.exceptions import ProductNotFoundError
from src.modules.products.repository import ProductRepository
from src.modules.users.enums import UserRole
from src.modules.users.models import User


class OrderService:
    def __init__(self, repository: OrderRepository, product_repository: ProductRepository) -> None:
        self.repository = repository
        self.product_repository = product_repository

    def get_all(self) -> list[Order]:
        return self.repository.get_all()

    def list_for_user(self, current_user: User) -> list[Order]:
        """ADMIN ve todas las órdenes; cualquier otro rol solo las suyas."""
        if current_user.role == UserRole.ADMIN:
            return self.repository.get_all()
        return self.repository.list_by_user(current_user.id)

    def get_owned_order(self, order_id: uuid.UUID, current_user: User) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)

        is_owner = order.user_id == current_user.id
        if not is_owner and current_user.role != UserRole.ADMIN:
            # 404 y no 403: no revelamos que la orden existe si no es tuya.
            raise OrderNotFoundError(order_id)

        return order

    def add_order(self, data: OrderCreate, user_id: uuid.UUID) -> Order:
        # El precio nunca sale del cliente: se toma del Product vigente en
        # el momento del pedido y queda congelado en OrderItem.unit_price.
        line_items: list[tuple[uuid.UUID, int, float]] = []
        total_amount = 0.0
        for item in data.items:
            product = self.product_repository.get_by_id(item.product_id)
            if product is None:
                raise ProductNotFoundError(item.product_id)

            unit_price = product.price
            total_amount += unit_price * item.quantity
            line_items.append((item.product_id, item.quantity, unit_price))

        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            order_status=OrderStatus.PENDING.value,
        )
        self.repository.add(order)

        for product_id, quantity, unit_price in line_items:
            self.repository.add_item(
                OrderItem(
                    order_id=order.id,
                    product_id=product_id,
                    quantity=quantity,
                    unit_price=unit_price,
                )
            )

        self.repository.commit()
        self.repository.refresh(order)
        logging.info("Orden creada: %s (usuario %s)", order.id, user_id)
        return order
