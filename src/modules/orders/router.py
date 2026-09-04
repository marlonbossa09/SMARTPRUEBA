import uuid

from fastapi import APIRouter, status

from src.modules.auth.dependencies import CurrentUser
from src.modules.orders.dependencies import OrderServiceDep
from src.modules.orders.schemas import OrderCreate, OrderRead

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, service: OrderServiceDep, current_user: CurrentUser) -> OrderRead:
    return service.add_order(order, current_user.id)


@router.get("/", response_model=list[OrderRead])
def read_orders(service: OrderServiceDep, current_user: CurrentUser) -> list[OrderRead]:
    """Un ADMIN ve todas las órdenes; cualquier otro rol solo ve las suyas."""
    return service.list_for_user(current_user)


@router.get("/{order_id}", response_model=OrderRead)
def read_order(order_id: uuid.UUID, service: OrderServiceDep, current_user: CurrentUser) -> OrderRead:
    return service.get_owned_order(order_id, current_user)
