from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.rate_limit import limiter
from src.modules.auth.dependencies import AuthServiceDep, CurrentUser
from src.modules.auth.schemas import RefreshRequest, TokenResponse
from src.modules.users.dependencies import UserServiceDep
from src.modules.users.schemas import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, service: UserServiceDep) -> UserRead:
    """Alta de usuario. Público: es el punto de entrada para crear una cuenta."""
    return service.register(data)


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Credenciales incorrectas"},
        status.HTTP_429_TOO_MANY_REQUESTS: {"description": "Demasiados intentos"},
    },
)
# slowapi lee la IP del objeto `Request`, por eso el parámetro es obligatorio
# aunque el handler no lo use.
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
) -> TokenResponse:
    return service.login(form_data.username, form_data.password)


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("10/minute")
def refresh(request: Request, data: RefreshRequest, service: AuthServiceDep) -> TokenResponse:
    return service.refresh(data.refresh_token)


@router.get("/me", response_model=UserRead)
def me(current_user: CurrentUser) -> UserRead:
    return current_user
