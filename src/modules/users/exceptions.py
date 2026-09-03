import uuid

from src.core.exceptions import AppError


class UserNotFoundError(AppError):
    status_code = 404
    detail = "User not found"

    def __init__(self, user_id: uuid.UUID | None = None) -> None:
        super().__init__(None if user_id is None else f"User with id {user_id} not found")


class EmailAlreadyExistsError(AppError):
    status_code = 409
    detail = "A user with that email already exists"
