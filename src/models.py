"""Registro central de modelos.

Alembic importa este módulo para que todas las tablas queden en
`Base.metadata` antes de comparar contra la base de datos. Cada modelo nuevo
debe añadirse aquí o el autogenerate no lo verá.
"""

from src.core.database import Base
from src.modules.users.models import User
from src.modules.products.models import Product

__all__ = ["Base", "User", "Product"]
