import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.modules.users.enums import UserRole

# bcrypt solo usa los primeros 72 bytes y >= 4.0 lanza ValueError si se excede;
# el límite se valida aquí para devolver un 422 claro en vez de un 500.
Password = Annotated[str, Field(min_length=8, max_length=72)]
Name = Annotated[str, Field(min_length=1, max_length=100)]


class UserCreate(BaseModel):
    email: EmailStr
    first_name: Name
    last_name: Name
    password: Password
    # Opcional: si no se envía, el usuario queda como customer.
    role: UserRole = UserRole.CUSTOMER


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
