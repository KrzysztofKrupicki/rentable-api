"""A module containing equipment-related routers."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.container import Container
from src.core.domain.equipment import Equipment, EquipmentBroker, EquipmentIn
from src.infrastructure.dto.equipmentdto import EquipmentDTO
from src.infrastructure.services.iequipment import IEquipmentService
from src.infrastructure.utils import consts

router = APIRouter()
bearer_scheme = HTTPBearer()

@router.post("/create", response_model=Equipment, status_code=201)
@inject
async def create_equipment(
    equipment: EquipmentIn,
    service: IEquipmentService = Depends(Provide[Container.equipment_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new equipment.

    Args:
        equipment (EquipmentIn): The equipment input data.
        service (IEquipmentService, optional): The injected equipment dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The created equipment attributes.
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
    
    extended_equipment_data = EquipmentBroker(
        equipment_owner_id=user_uuid,
        **equipment.model_dump(),
    )

    if new_equipment := await service.add_equipment(extended_equipment_data):
        return new_equipment.model_dump()


@router.get("/all", response_model=Iterable[Equipment], status_code=200)
@inject
async def get_all_equipment(
    service: IEquipmentService = Depends(Provide[Container.equipment_service]),
) -> Iterable[dict]:
    """An endpoint for getting all equipment.

    Args:
        service (IEquipmentService, optional): The injected equipment dependency.

    Returns:
        Iterable[dict]: The list of equipment DTOs.
    """
    equipment_list = await service.get_all_equipments()
    return equipment_list


@router.get("/{equipment_id}", response_model=Equipment, status_code=200)
@inject
async def get_equipment_by_id(
    equipment_id: int,
    service: IEquipmentService = Depends(Provide[Container.equipment_service]),
) -> dict:
    """An endpoint for getting equipment by id.

    Args:
        equipment_id (int): The equipment id.
        service (IEquipmentService, optional): The injected equipment dependency.

    Raises:
        HTTPException: 404 if equipment does not exist.

    Returns:
        dict: The equipment DTO.
    """
    if equipment := await service.get_equipment_by_id(equipment_id):
        return equipment

    raise HTTPException(
        status_code=404,
        detail="Equipment not found",
    )


@router.put("/{equipment_id}", response_model=Equipment, status_code=200)
@inject
async def update_equipment(
    equipment_id: int,
    equipment: EquipmentIn,
    service: IEquipmentService = Depends(Provide[Container.equipment_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating equipment.

    Args:
        equipment_id (int): The equipment id.
        equipment (EquipmentIn): The updated equipment data.
        service (IEquipmentService, optional): The injected equipment dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if equipment does not exist.

    Returns:
        dict: The updated equipment attributes.
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
    
    if equipment_data := await service.get_equipment_by_id(equipment_id=equipment_id):
        if(str(equipment_data.equipment_owner_id) != user_uuid):
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_updated_equipment = EquipmentBroker(
            equipment_owner_id=user_uuid,
            **equipment.model_dump(),
        )

        updated_equipment_data = await service.update_equipment(
            equipment_id=equipment_id,
            data=extended_updated_equipment,
        )

        return updated_equipment_data.model_dump() if updated_equipment_data else {}

    raise HTTPException(
        status_code=404,
        detail="Equipment not found",
    )


@router.delete("/{equipment_id}", status_code=204)
@inject
async def delete_equipment(
    equipment_id: int,
    service: IEquipmentService = Depends(Provide[Container.equipment_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting equipment.

    Args:
        equipment_id (int): The equipment id.
        service (IEquipmentService, optional): The injected equipment dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.
        
    Raises:
        HTTPException: 404 if equipment does not exist.
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
    
    if equipment_data := await service.get_equipment_by_id(equipment_id=equipment_id):
        if(str(equipment_data.equipment_owner_id) != user_uuid):
            raise HTTPException(status_code=403, detail="Unauthorized")

    if await service.get_equipment_by_id(equipment_id):
        await service.delete_equipment(equipment_id)
        return
    
    raise HTTPException(
        status_code=404,
        detail="Equipment not found",
    )


@router.get("/category/{category_id}", response_model=Iterable[Equipment], status_code=200)
@inject
async def get_all_equipment_by_category_id(
    category_id: int,
    service: IEquipmentService = Depends(Provide[Container.equipment_service]),
) -> Iterable:
    """An endpoint for getting all equipment by category id.

    Args:
        category_id (int): The category id.
        service (IEquipmentService, optional): The injected equipment dependency.

    Returns:
        Iterable[dict]: The list of equipment DTOs.
    """
    equipment_list = await service.get_all_equipment_by_category_id(category_id)
    return equipment_list


@router.get("/subcategory/{subcategory_id}", response_model=Iterable[Equipment], status_code=200)
@inject
async def get_all_equipment_by_subcategory_id(
    subcategory_id: int,
    service: IEquipmentService = Depends(Provide[Container.equipment_service]),
) -> Iterable:
    """An endpoint for getting all equipment by subcategory id.

    Args:
        subcategory_id (int): The subcategory id.
        service (IEquipmentService, optional): The injected equipment dependency.

    Returns:
        Iterable[dict]: The list of equipment DTOs.
    """
    equipment_list = await service.get_all_equipment_by_subcategory_id(subcategory_id)
    return equipment_list
