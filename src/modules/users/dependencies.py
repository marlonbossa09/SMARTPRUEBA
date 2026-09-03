from typing import Annotated

from fastapi import Depends

from src.core.database import DbSession
from src.modules.users.repository import UserRepository
from src.modules.users.service import UserService


def get_user_repository(db: DbSession) -> UserRepository:
    return UserRepository(db)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
