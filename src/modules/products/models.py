import uuid
from sqlalchemy import DateTime, ForeignKey, String, func
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.modules.users.models import User


class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255))
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    price: Mapped[float] = mapped_column()
    
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Unidireccional: Product conoce a User, pero User no navega a sus
    # products (para eso está ProductRepository.list_by_user). Evita el
    # ciclo de imports users<->products y respeta que "users" es el módulo
    # base del que dependen otros, nunca al revés.
    user: Mapped["User"] = relationship("User")