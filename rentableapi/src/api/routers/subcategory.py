"""A module containing subcategory endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.core.domain.subcategory import Subcategory, SubcategoryIn
from src.infrastructure.dto.subcategorydto import SubcategoryDTO
from src.infrastructure.services.isubcategory import ISubcategoryService
from src.infrastructure.utils import consts

bearer_scheme = HTTPBearer()
router = APIRouter()


@router.post("/create", response_model=Subcategory, status_code=201)
@inject
async def create_subcategory(
    subcategory: SubcategoryIn,
    service: ISubcategoryService = Depends(Provide[Container.subcategory_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new subcategory.

    Args:
        subcategory (SubcategoryIn): The subcategory data.
        service (ISubcategoryService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new subcategory attributes.
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

    new_subcategory = await service.add_subcategory(subcategory)
    return new_subcategory.model_dump() if new_subcategory else {}


@router.get("/all", response_model=Iterable[SubcategoryDTO], status_code=200)
@inject
async def get_all_subcategories(
    service: ISubcategoryService = Depends(Provide[Container.subcategory_service]),
) -> Iterable:
    """An endpoint for getting all subcategories.

    Args:
        service (ISubcategoryService, optional): The injected service dependency.

    Returns:
        Iterable: The subcategory attributes collection.
    """

    subcategories = await service.get_all_subcategories()
    return subcategories


@router.get(
    "/category/{category_id}", response_model=Iterable[SubcategoryDTO], status_code=200
)
@inject
async def get_all_subcategories_by_category_id(
    category_id: int,
    service: ISubcategoryService = Depends(Provide[Container.subcategory_service]),
) -> Iterable:
    """An endpoint for getting all subcategories by category id.

    Args:
        category_id (int): The id of the category.
        service (ISubcategoryService, optional): The injected service dependency.

    Returns:
        Iterable: The subcategory attributes collection.
    """

    subcategories = await service.get_all_subcategories_by_category_id(category_id)
    return subcategories


@router.get("/{subcategory_id}", response_model=SubcategoryDTO, status_code=200)
@inject
async def get_subcategory_by_id(
    subcategory_id: int,
    service: ISubcategoryService = Depends(Provide[Container.subcategory_service]),
) -> dict | None:
    """An endpoint for getting subcategory by id.

    Args:
        subcategory_id (int): The id of the subcategory.
        service (ISubcategoryService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if subcategory does not exist.

    Returns:
        dict | None: The subcategory details.
    """

    if subcategory := await service.get_subcategory_by_id(subcategory_id):
        return subcategory.model_dump()

    raise HTTPException(status_code=404, detail="Subcategory not found")


@router.put("/{subcategory_id}", response_model=Subcategory, status_code=201)
@inject
async def update_subcategory(
    subcategory_id: int,
    updated_subcategory: SubcategoryIn,
    service: ISubcategoryService = Depends(Provide[Container.subcategory_service]),
) -> dict:
    """An endpoint for updating subcategory data.

    Args:
        subcategory_id (int): The id of the subcategory.
        updated_subcategory (SubcategoryIn): The updated subcategory details.
        service (ISubcategoryService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if subcategory does not exist.

    Returns:
        dict: The updated subcategory details.
    """
    if await service.get_subcategory_by_id(subcategory_id=subcategory_id):
        new_updated_subcategory = await service.update_subcategory(
            subcategory_id=subcategory_id,
            data=updated_subcategory,
        )
        return new_updated_subcategory.model_dump() if new_updated_subcategory else {}

    raise HTTPException(status_code=404, detail="Subcategory not found")


@router.delete("/{subcategory_id}", status_code=204)
@inject
async def delete_subcategory(
    subcategory_id: int,
    service: ISubcategoryService = Depends(Provide[Container.subcategory_service]),
) -> None:
    """An endpoint for deleting subcategories.

    Args:
        subcategory_id (int): The id of the subcategory.
        service (ISubcategoryService): The injected service dependency.

    Raises:
        HTTPException: 404 if subcategory does not exist.

    Returns:
        dict: Empty if operation finished.
    """
    if await service.get_subcategory_by_id(subcategory_id=subcategory_id):
        await service.delete_subcategory(subcategory_id)
        return

    raise HTTPException(status_code=404, detail="Subcategory not found")
