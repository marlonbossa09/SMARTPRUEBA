from src.core.exceptions import AppError


class InvalidCredentialsError(AppError):
    status_code = 401
    # Mensaje deliberadamente genérico: no revela si el email existe.
    detail = "Incorrect email or password"


class InactiveUserError(AppError):
    status_code = 403
    detail = "Inactive user"


class InvalidTokenError(AppError):
    status_code = 401
    detail = "Could not validate credentials"


class InsufficientPermissionsError(AppError):
    status_code = 403
    detail = "No tienes permiso para realizar esta acción"
