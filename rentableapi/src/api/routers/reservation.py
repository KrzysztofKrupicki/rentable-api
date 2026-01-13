"""A module containing reservation-related routers."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from pydantic import UUID4

from src.container import Container
from src.core.domain.reservation import Reservation, ReservationBroker, ReservationIn
from src.infrastructure.services.iequipment import IEquipmentService
from src.infrastructure.services.ireservation import IReservationService
from src.infrastructure.utils import consts

router = APIRouter(tags=["Reservation"])
bearer_scheme = HTTPBearer()


@router.post("/create", response_model=Reservation, status_code=201)
@inject
async def create_reservation(
    reservation: ReservationIn,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new reservation.

    Args:
        reservation (ReservationIn): The reservation input data.
        service (IReservationService, optional): The injected reservation service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The created reservation attributes.
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

    total_price = await service.calculate_total_price(
        equipment_id=reservation.equipment_id,
        start_date=reservation.start_date,
        end_date=reservation.end_date,
    )

    extended_reservation_data = ReservationBroker(
        user_id=user_uuid,
        total_price=total_price,
        **reservation.model_dump(),
    )

    if new_reservation := await service.add_reservation(extended_reservation_data):
        return new_reservation.model_dump()


@router.get("/all", response_model=Iterable[Reservation], status_code=200)
@inject
async def get_all_reservations(
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable[dict]:
    """An endpoint for getting all reservations.

    Args:
        service (IReservationService, optional): The injected reservation service.

    Returns:
        Iterable[dict]: The list of reservation DTOs.
    """
    reservation_list = await service.get_all_reservations()
    return reservation_list


@router.get("/{reservation_id}", response_model=Reservation, status_code=200)
@inject
async def get_reservation_by_id(
    reservation_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict:
    """An endpoint for getting reservation by id.

    Args:
        reservation_id (int): The reservation id.
        service (IReservationService, optional): The injected reservation service.

    Raises:
        HTTPException: 404 if reservation does not exist.

    Returns:
        dict: The reservation DTO.
    """
    if reservation := await service.get_reservation_by_id(reservation_id):
        return reservation

    raise HTTPException(status_code=404, detail="Reservation not found")


@router.put("/{reservation_id}", response_model=Reservation, status_code=200)
@inject
async def update_reservation(
    reservation_id: int,
    reservation: ReservationIn,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    equipment_service: IEquipmentService = Depends(
        Provide[Container.equipment_service]
    ),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating reservation.

    Args:
        reservation_id (int): The reservation id.
        reservation (ReservationIn): The reservation input data.
        service (IReservationService, optional): The injected reservation service.
        equipment_service (IEquipmentService, optional): The injected equipment service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if reservation does not exist.

    Returns:
        dict: The updated reservation attributes.
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

    if reservation_data := await service.get_reservation_by_id(
        reservation_id=reservation_id
    ):
        is_owner = str(reservation_data.user_id) == user_uuid

        equipment = await equipment_service.get_equipment_by_id(
            reservation_data.equipment_id
        )
        is_equipment_owner = False
        if equipment:
            is_equipment_owner = str(equipment.equipment_owner_id) == user_uuid

        if not (is_owner or is_equipment_owner):
            raise HTTPException(status_code=403, detail="Unauthorized")

        total_price = await service.calculate_total_price(
            equipment_id=reservation.equipment_id,
            start_date=reservation.start_date,
            end_date=reservation.end_date,
        )

        extended_updated_reservation = ReservationBroker(
            user_id=user_uuid,
            total_price=total_price,
            **reservation.model_dump(),
        )

        updated_reservation_data = await service.update_reservation(
            reservation_id=reservation_id,
            data=extended_updated_reservation,
        )

        return updated_reservation_data.model_dump() if updated_reservation_data else {}

    raise HTTPException(
        status_code=404,
        detail="Reservation not found",
    )


@router.delete("/{reservation_id}", status_code=204)
@inject
async def delete_reservation(
    reservation_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting reservation.

    Args:
        reservation_id (int): The reservation id.
        service (IReservationService, optional): The injected reservation service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if reservation does not exist.
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

    if reservation_data := await service.get_reservation_by_id(
        reservation_id=reservation_id
    ):
        if str(reservation_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

    if await service.get_reservation_by_id(reservation_id):
        await service.delete_reservation(reservation_id)
        return

    raise HTTPException(
        status_code=404,
        detail="Reservation not found",
    )


@router.get("/user/{user_id}", response_model=Iterable[Reservation], status_code=200)
@inject
async def get_all_reservations_by_user(
    user_id: UUID4,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable[dict]:
    """An endpoint for getting all reservations by user id.

    Args:
        user_id (UUID4): The user UUID4.
        service (IReservationService, optional): The injected reservation service.

    Returns:
        Iterable[dict]: The list of reservation DTOs.
    """
    reservation_list = await service.get_all_reservations_by_user(user_id)
    return reservation_list


@router.get(
    "/category/{category_id}", response_model=Iterable[Reservation], status_code=200
)
@inject
async def get_all_reservation_by_category_id(
    category_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable[dict]:
    """An endpoint for getting all reservations by category id.

    Args:
        category_id (int): The category id.
        service (IReservationService, optional): The injected reservation service.

    Returns:
        Iterable[dict]: The list of reservation DTOs.
    """
    reservation_list = await service.get_all_reservation_by_category_id(category_id)
    return reservation_list


@router.get(
    "/subcategory/{subcategory_id}",
    response_model=Iterable[Reservation],
    status_code=200,
)
@inject
async def get_all_reservation_by_subcategory_id(
    subcategory_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable[dict]:
    """An endpoint for getting all reservations by subcategory id.

    Args:
        subcategory_id (int): The subcategory id.
        service (IReservationService, optional): The injected reservation service.

    Returns:
        Iterable[dict]: The list of reservation DTOs.
    """
    reservation_list = await service.get_all_reservation_by_subcategory_id(
        subcategory_id
    )
    return reservation_list


@router.get(
    "/equipment/{equipment_id}", response_model=Iterable[Reservation], status_code=200
)
@inject
async def get_all_reservations_by_equipment_id(
    equipment_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable[dict]:
    """An endpoint for getting all reservations by equipment id.

    Args:
        equipment_id (int): The equipment id.
        service (IReservationService, optional): The injected reservation service.

    Returns:
        Iterable[dict]: The list of reservation DTOs.
    """
    reservation_list = await service.get_all_reservations_by_equipment_id(equipment_id)
    return reservation_list


@router.get("/most_rented/{limit}", response_model=Iterable[dict], status_code=200)
@inject
async def get_most_rented_equipment_ids(
    limit: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable[dict]:
    """An endpoint for getting most rented equipment IDs.

    Args:
        limit (int): The limit of the most rented equipment IDs.
        service (IReservationService, optional): The injected reservation service.

    Returns:
        Iterable[dict]: The list of most rented equipment IDs.
    """
    return await service.get_most_rented_equipment_ids(limit)
