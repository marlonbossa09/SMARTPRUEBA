from typing import Annotated

from fastapi import Depends

from src.core.database import DbSession
from src.modules.orders.repository import OrderRepository
from src.modules.orders.service import OrderService
from src.modules.products.dependencies import ProductRepositoryDep


def get_order_repository(db: DbSession) -> OrderRepository:
    return OrderRepository(db)


OrderRepositoryDep = Annotated[OrderRepository, Depends(get_order_repository)]


def get_order_service(
    order_repository: OrderRepositoryDep,
    product_repository: ProductRepositoryDep,
) -> OrderService:
    return OrderService(order_repository, product_repository)


OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
