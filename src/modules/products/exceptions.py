import uuid

from src.core.exceptions import AppError

class ProductNotFoundError(AppError):
    status_code = 404
    detail = "Producto no encontrado"
    
    def __init__(self, product_id: uuid.UUID | None = None) -> None:
        super().__init__(None if product_id is None else f"Producto con id {product_id} no encontrado") 

class ProductAlreadyExistsException(AppError):
    status_code = 409
    detail = "Ya existe un producto con ese nombre"
    
    def __init__(self, product_name: str | None = None) -> None:
        super().__init__(None if product_name is None else f"Ya existe un producto con ese nombre: {product_name}")
         