from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    # Sin `min_length`: en login no se valida la fuerza de la contraseña, solo
    # el techo de bcrypt. Un mínimo aquí filtraría credenciales antiguas.
    password: Annotated[str, Field(max_length=72)]
    


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
