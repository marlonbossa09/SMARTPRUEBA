from typing import Annotated, Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.modules.auth.exceptions import InsufficientPermissionsError, InvalidTokenError
from src.modules.auth.service import AuthService
from src.modules.users.dependencies import UserRepositoryDep
from src.modules.users.enums import UserRole
from src.modules.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_auth_service(repository: UserRepositoryDep) -> AuthService:
    return AuthService(repository)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_current_user(
    service: AuthServiceDep,
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> User:
    if token is None:
        raise InvalidTokenError("Not authenticated")
    return service.get_user_from_access_token(token)


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_roles(*allowed_roles: UserRole) -> Callable[[User], User]:
    """Fábrica de dependencias para autorización por rol.

    Uso: `current_user: Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.SELLER))]`
    Cualquiera de los roles pasados es suficiente (OR): un usuario solo tiene
    un rol a la vez, así que "ADMIN o SELLER" es la única lectura posible.
    """

    def check_role(current_user: CurrentUser) -> User:
        if current_user.role not in allowed_roles:
            raise InsufficientPermissionsError()
        return current_user

    return check_role
