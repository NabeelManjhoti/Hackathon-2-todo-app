"""FastAPI application entry point."""

import json
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.config import settings
from src.database import create_db_and_tables
from src.routers import health, tasks

# Configure structured logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(message)s',
)
logger = logging.getLogger(__name__)


class StructuredLogger:
    """Structured JSON logger for consistent log formatting."""

    @staticmethod
    def log(level: str, message: str, **kwargs: object) -> None:
        """Log a structured JSON message.

        Args:
            level: Log level (INFO, ERROR, etc.)
            message: Log message
            **kwargs: Additional fields to include in log
        """
        log_data = {
            "level": level,
            "message": message,
            **kwargs,
        }
        logger.log(getattr(logging, level), json.dumps(log_data))


structured_logger = StructuredLogger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.

    Handles startup and shutdown events.

    Args:
        app: FastAPI application instance

    Yields:
        None
    """
    # Startup
    structured_logger.log("INFO", "Starting application")
    await create_db_and_tables()
    structured_logger.log("INFO", "Database tables created")
    yield
    # Shutdown
    structured_logger.log("INFO", "Shutting down application")


# Create FastAPI application
app = FastAPI(
    title="Todo Backend API",
    description="RESTful API for task management with CRUD operations and database persistence",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS middleware (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handle HTTP exceptions with consistent error format.

    Args:
        request: The incoming request
        exc: The HTTP exception

    Returns:
        JSON response with error detail
    """
    structured_logger.log(
        "ERROR",
        "HTTP exception",
        status_code=exc.status_code,
        detail=str(exc.detail),
        path=request.url.path,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors with detailed error information.

    Args:
        request: The incoming request
        exc: The validation error

    Returns:
        JSON response with validation error details
    """
    structured_logger.log(
        "ERROR",
        "Validation error",
        path=request.url.path,
        errors=exc.errors(),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions with generic error response.

    Args:
        request: The incoming request
        exc: The exception

    Returns:
        JSON response with generic error message
    """
    structured_logger.log(
        "ERROR",
        "Internal server error",
        path=request.url.path,
        error=str(exc),
        error_type=type(exc).__name__,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


# Request/response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses.

    Args:
        request: The incoming request
        call_next: The next middleware or route handler

    Returns:
        The response from the next handler
    """
    structured_logger.log(
        "INFO",
        "Request received",
        method=request.method,
        path=request.url.path,
    )
    response = await call_next(request)
    structured_logger.log(
        "INFO",
        "Response sent",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
    )
    return response


# Register routers
app.include_router(health.router)
app.include_router(tasks.router)  # type: ignore[has-type]
