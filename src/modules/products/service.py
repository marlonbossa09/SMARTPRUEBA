import uuid

from sqlalchemy.exc import IntegrityError


from src.modules.products.exceptions import ProductAlreadyExistsException, ProductNotFoundError
from src.modules.products.repository import ProductRepository
from src.modules.products.models import Product
from src.modules.products.schemas import ProductCreate

class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository
        
    def get_all(self) -> list[Product]:
        return self.repository.get_all()
    
    def get_by_id(self, product_id: uuid.UUID) -> Product:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product
    
    def get_by_name(self, name: str) -> Product:
        product = self.repository.get_by_name(name)
        if product is None:
            raise ProductNotFoundError()
        return product
    
    def add_product(self, product: ProductCreate, user_id: uuid.UUID) -> Product:
        name = product.name.lower()
        if self.repository.exists_by_name(name):
            raise ProductAlreadyExistsException()
        new_product = Product(
            name=name,
            description=product.description,
            price=product.price,
            user_id=user_id,
        )

        try:
            self.repository.add(new_product)
            self.repository.commit()
        except IntegrityError:
            self.repository.rollback()
            raise ProductAlreadyExistsException() from None

        self.repository.refresh(new_product)
        return new_product
    
    
        
        