import logging

from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.core.database import DbSession

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    database: str


@router.get("/", summary="Bienvenido a SMARTPRUEBA", status_code=status.HTTP_200_OK)
def api_functional() -> dict[str, str]:
    return {"status": "Funcional"}

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Estado del servicio y de la base de datos",
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": HealthResponse,
            "description": "La base de datos no responde",
        }
    },
)
def health_check(db: DbSession, response: Response) -> HealthResponse:
    """Devuelve 200 si la API responde y la base de datos acepta consultas,
    503 en caso contrario. Lo usan el healthcheck de Docker y el balanceador.
    """
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as e:
        logging.error(f"Health check failed, database unreachable: {str(e)}")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthResponse(status="unhealthy", database="unreachable")

    return HealthResponse(status="healthy", database="connected")
