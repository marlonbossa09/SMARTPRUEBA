from fastapi import FastAPI

from src.api import register_routes
from src.core.config import settings
from src.core.exceptions import register_exception_handlers
from src.core.logging import configure_logging
from src.core.rate_limit import register_rate_limiting

configure_logging(settings.LOG_LEVEL)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

register_rate_limiting(app)
register_exception_handlers(app)
register_routes(app)
