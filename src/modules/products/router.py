import uuid

from fastapi import APIRouter

from src.modules.auth.dependencies import CurrentUser
from src.modules.products.dependencies import ProductServiceDep
from src.modules.products.schemas import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model= list[ProductRead])
def read_products(service: ProductServiceDep, current_user: CurrentUser) -> list[ProductRead]:
    return service.get_all()

@router.get("/{product_id}", response_model=ProductRead)
def read_product(product_id: uuid.UUID, service: ProductServiceDep, current_user: CurrentUser) -> ProductRead:
    return service.get_by_id(product_id)

@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, service: ProductServiceDep, current_user: CurrentUser) -> ProductRead:
    return service.add_product(product, current_user.id)