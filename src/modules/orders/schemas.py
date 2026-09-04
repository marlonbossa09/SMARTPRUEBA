import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from src.modules.orders.enums import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: Annotated[int, Field(gt=0, description="La cantidad debe ser mayor que cero")]


class OrderCreate(BaseModel):
    # user_id sale del usuario autenticado, no del cliente. El precio y el
    # total se calculan en el servicio a partir del Product real, nunca se
    # confía en lo que mande el cliente.
    items: Annotated[list[OrderItemCreate], Field(min_length=1)]


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    unit_price: float


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    total_amount: float
    order_status: OrderStatus
    created_at: datetime
    items: list[OrderItemRead]
