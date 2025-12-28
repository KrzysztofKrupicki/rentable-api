"""A module containing category endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.core.domain.category import Category, CategoryIn
from src.infrastructure.dto.categorydto import CategoryDTO
from src.infrastructure.services.icategory import ICategoryService
from src.infrastructure.utils import consts

bearer_scheme = HTTPBearer()
router = APIRouter()

@router.post("/create", response_model=Category, status_code=201)
@inject
async def create_category(
    category: CategoryIn,
    service: ICategoryService = Depends(Provide[Container.category_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new category.
    
    Args:
        category (CategoryIn): The category data.
        service (ICategoryService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new category attributes.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    new_category = await service.add_category(category)

    return new_category.model_dump() if new_category else {}


@router.get("/all", response_model=Iterable[CategoryDTO], status_code=200)
@inject
async def get_all_categories(
    service: ICategoryService = Depends(Provide[Container.category_service]),
) -> Iterable:
    """An endpoint for getting all categories.

    Args:
        service (ICategoryService, optional): The injected service dependency.

    Returns:
        Iterable: The category attributes collection.
    """

    categories = await service.get_all_categories()
    return categories

@router.get("/{category_id}", response_model=CategoryDTO, status_code=200)
@inject
async def get_category_by_id(
    category_id: int,
    service: ICategoryService = Depends(Provide[Container.category_service]),
) -> dict | None:
    """An endpoint for getting category by id.

    Args:
        category_id (int): The id of the category.
        service (ICategoryService, optional): The injected service dependency.

    Returns:
        dict | None: The category details.
    """

    if category := await service.get_category_by_id(category_id):
        return category.model_dump()
    
    raise HTTPException(status_code=404, detail="Category not found")


@router.put("/{category_id}", response_model=Category, status_code=201)
@inject
async def update_category(
    category_id: int,
    updated_category: CategoryIn,
    service: ICategoryService = Depends(Provide[Container.category_service]),
) -> dict:
    """An endpoint for updating category data.
    
    Args:
        category_id (int): The if of the category.
        updated_category (CategoryIn): The updated category details.
        service (ICategoryService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if category does nto exist.

    Returns:
        dict: The updated category details.
    """
    if await service.get_category_by_id(category_id=category_id):
        new_updated_category = await service.update_category(
            category_id=category_id,
            data=updated_category,
        )
        return new_updated_category.model_dump() if new_updated_category else {}
    raise HTTPException(status_code=404, details="Category not found")


@router.delete("/{category_id}", status_code=204)
@inject
async def delete_category(
    category_id: int,
    service: ICategoryService = Depends(Provide[Container.category_service]),
) -> None:
    """An endpoint for deleting categories.
    
    Args:
        category_id (int): The id of the category.
        servce (ICategoryService): The injected service dependency.

    Raises:
        HTTPException: 404 if category does not exist.
    
    Returns:
        dict: Empty if operation finished.
    """
    if await service.get_category_by_id(category_id=category_id):
        await service.delete_category(category_id)
        return
    
    raise HTTPException(status_code=404, detail="Category not found")