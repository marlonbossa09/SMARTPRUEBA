import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Excepción base del dominio.

    Los servicios lanzan subclases de esto, nunca `HTTPException`: así la capa
    de negocio no depende de FastAPI y se puede testear sin levantar la API.
    El handler registrado abajo la traduce a respuesta HTTP.
    """

    status_code: int = 500
    detail: str = "Internal server error"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        if exc.status_code >= 500:
            logging.error("%s en %s: %s", type(exc).__name__, request.url.path, exc.detail)
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
