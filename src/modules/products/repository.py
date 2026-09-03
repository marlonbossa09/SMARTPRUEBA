import uuid

from sqlalchemy import select
from src.modules.products.models import Product
from sqlalchemy.orm import Session

from src.modules.users.models import User

class ProductRepository:
    """ Puerta de entrada para Products. Ningún router ni servicio debe escribir queries SQLAlchemy fuera de aquí."""
    
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_all(self) -> list[Product]:
        return self._db.scalars(select(Product)).all()

    def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        return self._db.get(Product, product_id)

    def get_by_name(self, name: str) -> Product | None:
        return self._db.scalar(select(Product).where(Product.name == name))

    def exists_by_name(self, name: str) -> bool:
        return self._db.scalar(select(Product.id).where(Product.name == name)) is not None

    def add(self, product: Product) -> Product:
        self._db.add(product)
        self._db.flush()
        return product

    # --- Límites de transacción (unit of work mínima) ---

    def commit(self) -> None:
        self._db.commit()

    def rollback(self) -> None:
        self._db.rollback()

    def refresh(self, user: User) -> None:
        self._db.refresh(user)
