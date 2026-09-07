from typing import Annotated
from fastapi import APIRouter, Depends, Query, status

from src.modules.catalogs.schemas import CatalogResponse
from src.modules.catalogs.service import PublicCatalogsService

router = APIRouter(prefix="/public", tags=["Catalogs"])

# Inyección de dependencia del servicio (ajusta según la configuración de tus dependencias)
CatalogServiceDep = Annotated[PublicCatalogsService, Depends(PublicCatalogsService)]


@router.get("/catalogs", summary="Catálogos del sistema",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str] | dict[str, dict[str, str]],
)
def public_catalogs(service: CatalogServiceDep, 
    type_catalog: Annotated[
        str | None, 
        Query(description="Tipo de catálogo a consultar: 'orders', 'logs', 'users'")
    ] = None,
):
    """Devuelve los valores de los catálogos registrados (OrderStatus, LogLevels, UserRole)."""
    if type_catalog:
        return service.get_catalog_by_type(type_catalog)
    
    return service.get_all_catalogs()