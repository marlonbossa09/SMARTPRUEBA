from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.modules.auth.exceptions import InvalidTokenError
from src.modules.auth.service import AuthService
from src.modules.users.dependencies import UserRepositoryDep
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
