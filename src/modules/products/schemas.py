import uuid
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: str
    description: str
    create_at: datetime
    price: float
    user_id: uuid.UUID
    