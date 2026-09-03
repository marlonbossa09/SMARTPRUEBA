import uuid

from fastapi import APIRouter

from src.modules.auth.dependencies import CurrentUser
from src.modules.users.dependencies import UserServiceDep
from src.modules.users.schemas import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserRead])
def read_users(service: UserServiceDep, current_user: CurrentUser) -> list[UserRead]:
    return service.get_all()

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: uuid.UUID, service: UserServiceDep, current_user: CurrentUser) -> UserRead:
    return service.get_by_id(user_id)
