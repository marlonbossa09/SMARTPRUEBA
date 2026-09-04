import uuid

from src.core.exceptions import AppError

class OrderNotFoundError(AppError):
    status_code = 404
    detail = "Orden no encontrada"
    
    def __init__(self, order_id: uuid.UUID | None = None) -> None:
        super().__init__(None if order_id is None else f"Orden con id {order_id} no encontrada")
        
class OrderItemNotFoundError(AppError):
    status_code = 404
    detail = "Item de orden no encontrado"
    
    def __init__(self, order_item_id: uuid.UUID | None = None) -> None:
        super().__init__(None if order_item_id is None else f"Item de orden con id {order_item_id} no encontrado")    