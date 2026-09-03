import logging
import uuid
from typing import Any

import bcrypt
import jwt

from src.core.security import (
    TokenType,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from src.modules.auth.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from src.modules.auth.schemas import TokenResponse
from src.modules.users.models import User
from src.modules.users.repository import UserRepository

# Hash descartable para gastar el mismo tiempo cuando el email no existe y no
# filtrar por latencia qué correos están registrados.
_DUMMY_HASH = bcrypt.hashpw(b"dummy-password", bcrypt.gensalt()).decode("utf-8")


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def authenticate(self, email: str, password: str) -> User:
        user = self.repository.get_by_email(email.lower())

        if user is None:
            verify_password(password, _DUMMY_HASH)
            raise InvalidCredentialsError()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InactiveUserError()

        return user

    def login(self, username: str, password: str) -> TokenResponse:
        # OAuth2PasswordRequestForm no tiene noción de "email": en este
        # sistema el username del flujo OAuth2 ES el correo electrónico.
        user = self.authenticate(email=username, password=password)
        logging.info("Login correcto: %s", user.id)
        return self._issue_tokens(user.id)

    def refresh(self, refresh_token: str) -> TokenResponse:
        payload = self.decode(refresh_token, expected_type="refresh")
        user = self.repository.get_by_id(uuid.UUID(payload["sub"]))

        if user is None:
            raise InvalidTokenError()
        if not user.is_active:
            raise InactiveUserError()

        return self._issue_tokens(user.id)

    def get_user_from_access_token(self, token: str) -> User:
        payload = self.decode(token, expected_type="access")
        user = self.repository.get_by_id(uuid.UUID(payload["sub"]))

        if user is None:
            raise InvalidTokenError()
        if not user.is_active:
            raise InactiveUserError()

        return user

    def decode(self, token: str, expected_type: TokenType) -> dict[str, Any]:
        try:
            payload = decode_token(token)
        except jwt.PyJWTError:
            raise InvalidTokenError() from None

        # Sin esta comprobación, un refresh token serviría como access token.
        if payload.get("type") != expected_type:
            raise InvalidTokenError()

        try:
            uuid.UUID(payload["sub"])
        except (KeyError, ValueError, TypeError):
            raise InvalidTokenError() from None

        return payload

    @staticmethod
    def _issue_tokens(user_id: uuid.UUID) -> TokenResponse:
        return TokenResponse(
            access_token=create_access_token(user_id),
            refresh_token=create_refresh_token(user_id),
        )
