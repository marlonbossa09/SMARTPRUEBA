import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modules.users.models import User


class UserRepository:
    """Única puerta de acceso a la tabla `users`. Ningún router ni servicio
    debe escribir queries SQLAlchemy fuera de aquí.

    El repositorio NO hace commit: solo `flush()` para que la BD valide
    constraints. Quién confirma o revierte la transacción es el servicio, que
    es el que conoce la operación de negocio completa.
    """

    def __init__(self, db: Session) -> None:
        self._db = db
        
    def get_all(self) -> list[User]:
        return self._db.scalars(select(User)).all()

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self._db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self._db.scalar(select(User).where(User.email == email))

    def exists_by_email(self, email: str) -> bool:
        return self._db.scalar(select(User.id).where(User.email == email)) is not None

    def add(self, user: User) -> User:
        self._db.add(user)
        self._db.flush()
        return user

    # --- Límites de transacción (unit of work mínima) ---

    def commit(self) -> None:
        self._db.commit()

    def rollback(self) -> None:
        self._db.rollback()

    def refresh(self, user: User) -> None:
        self._db.refresh(user)
