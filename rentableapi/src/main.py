"""Main module of the app."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from src.api.routers.category import router as category_router
from src.api.routers.equipment import router as equipment_router
from src.api.routers.equipment_review import router as equipment_review_router
from src.api.routers.reservation import router as reservation_router
from src.api.routers.subcategory import router as subcategory_router
from src.api.routers.user_review import router as user_review_router
from src.api.routers.user import router as user_router
from src.container import Container
from src.db import database, init_db

container = Container()
container.wire(
    modules=[
        "src.api.routers.category",
        "src.api.routers.subcategory",
        "src.api.routers.user",
        "src.api.routers.equipment",
        "src.api.routers.reservation",
        "src.api.routers.equipment_review",
        "src.api.routers.user_review",
    ]
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(category_router, prefix="/category")
app.include_router(subcategory_router, prefix="/subcategory")
app.include_router(user_router, prefix="/user")
app.include_router(equipment_router, prefix="/equipment")
app.include_router(reservation_router, prefix="/reservation")
app.include_router(equipment_review_router, prefix="/equipment_review")
app.include_router(user_review_router, prefix="/user_review")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)
