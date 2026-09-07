from fastapi import APIRouter, FastAPI

from src.health.router import router as health_router
from src.modules.auth.router import router as auth_router
from src.modules.users.router import router as users_router
from src.modules.products.router import router as products_router
from src.modules.orders.router import router as order_router
from src.modules.catalogs.router import router as catalogs_router

def register_routes(app: FastAPI) -> None:
    api_v1 = APIRouter(prefix="/api/v1")

    app.include_router(health_router)
    api_v1.include_router(auth_router)
    api_v1.include_router(users_router)
    api_v1.include_router(products_router)
    api_v1.include_router(order_router)
    app.include_router(catalogs_router)

    app.include_router(api_v1)