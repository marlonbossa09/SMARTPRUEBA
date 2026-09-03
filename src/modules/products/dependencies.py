from typing import Annotated

from fastapi import Depends

from src.core.database import DbSession
from src.modules.products.repository import ProductRepository
from src.modules.products.service import ProductService


def get_product_repository(db: DbSession) -> ProductRepository:
    return ProductRepository(db)

ProductRepositoryDep = Annotated[ProductRepository, Depends(get_product_repository)]


def get_product_service(product_repository: ProductRepositoryDep) -> ProductService:
    return ProductService(product_repository)

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
