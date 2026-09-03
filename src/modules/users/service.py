import logging
import uuid

from sqlalchemy.exc import IntegrityError

from src.core.security import hash_password
from src.modules.users.exceptions import EmailAlreadyExistsError, UserNotFoundError
from src.modules.users.models import User
from src.modules.users.repository import UserRepository
from src.modules.users.schemas import UserCreate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
        
    def get_all(self) -> list[User]:
        return self.repository.get_all()

    def get_by_id(self, user_id: uuid.UUID) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

    def register(self, data: UserCreate) -> User:
        email = data.email.lower()
        if self.repository.exists_by_email(email):
            raise EmailAlreadyExistsError()

        user = User(
            email=email,
            first_name=data.first_name,
            last_name=data.last_name,
            password_hash=hash_password(data.password),
        )

        try:
            self.repository.add(user)
            self.repository.commit()
        except IntegrityError:
            # Dos registros simultáneos con el mismo email: el chequeo previo
            # pasó en ambos y aquí gana el índice único.
            self.repository.rollback()
            raise EmailAlreadyExistsError() from None

        self.repository.refresh(user)
        logging.info("Usuario registrado: %s", user.id)
        return user
