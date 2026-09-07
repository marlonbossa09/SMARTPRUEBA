from enum import StrEnum
from fastapi import HTTPException, status

from src.core.logging import LogLevels
from src.modules.orders.enums import OrderStatus
from src.modules.users.enums import UserRole


class PublicCatalogsService:
    # Mapeo centralizado de los catálogos disponibles en la app
    _CATALOGS: dict[str, type[StrEnum]] = {
        "orders": OrderStatus,
        "logs": LogLevels,
        "users": UserRole,
    }

    def get_catalog_by_type(self, type_catalog: str) -> dict[str, str]:
        """Retorna las claves y valores del catálogo solicitado en formato Key-Value."""
        catalog_enum = self._CATALOGS.get(type_catalog.lower())
        
        if not catalog_enum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Catálogo '{type_catalog}' no encontrado. Disponibles: {list(self._CATALOGS.keys())}"
            )

        # Convierte el Enum a un diccionario: {"PENDING": "pending", "PAID": "paid", ...}
        return {enum_item.name: enum_item.value for enum_item in catalog_enum}

    def get_all_catalogs(self) -> dict[str, dict[str, str]]:
        """Retorna todos los catálogos del sistema agrupados."""
        return {
            catalog_name: {enum_item.name: enum_item.value for enum_item in enum_cls}
            for catalog_name, enum_cls in self._CATALOGS.items()
        }