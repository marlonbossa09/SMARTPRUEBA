from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, status

from src.modules.auth.dependencies import CurrentUser, require_roles
from src.modules.orders.dependencies import OrderServiceDep
from src.modules.orders.schemas import OrderCreate, OrderRead, OrderStatusUpdate
from src.modules.orders.service import OrderService
from src.modules.users.enums import UserRole
from src.modules.users.models import User

router = APIRouter(prefix="/orders", tags=["Orders"])

AdminOrSellerUser = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.SELLER))]

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

@router.patch("/{order_id}/status", response_model=OrderRead)
def change_order_status(
    order_id: uuid.UUID,
    status_data: OrderStatusUpdate,
    service: OrderServiceDep,
    current_user: AdminOrSellerUser,
) -> OrderRead:
    return service.change_order_status(
        order_id=order_id,
        new_status=status_data.order_status,
        current_user=current_user,
    )