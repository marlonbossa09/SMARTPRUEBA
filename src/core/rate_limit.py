from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

# Almacenamiento en memoria: el contador es por proceso, así que con varios
# workers el límite real se multiplica. Para producción, apuntar a Redis con
# `storage_uri="redis://..."`.
limiter = Limiter(key_func=get_remote_address)


def register_rate_limiting(app: FastAPI) -> None:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
