"""A module containing equipment review-related routers."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from pydantic import UUID4

from src.container import Container
from src.core.domain.equipment_review import (
    EquipmentReview,
    EquipmentReviewIn,
    EquipmentReviewBroker,
)
from src.infrastructure.dto.equipment_reviewdto import EquipmentReviewDTO
from src.infrastructure.services.iequipment_review import IEquipmentReviewService
from src.infrastructure.utils import consts

bearer_scheme = HTTPBearer()
router = APIRouter(tags=["Equipment Review"])


@router.post("/create", response_model=EquipmentReview, status_code=201)
@inject
async def create_equipment_review(
    review: EquipmentReviewIn,
    service: IEquipmentReviewService = Depends(
        Provide[Container.equipment_review_service]
    ),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new equipment review.

    Args:
        review (EquipmentReviewIn): The equipment review data.
        service (IEquipmentReviewService, optional): The injected equipment review dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if unauthorized.

    Returns:
        dict: The created equipment review attributes.
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

    extended_equipment_review_data = EquipmentReviewBroker(
        reviewer_id=user_uuid,
        **review.model_dump(),
    )

    if new_equipment_review := await service.add_equipment_review(
        extended_equipment_review_data
    ):
        return new_equipment_review.model_dump()


@router.get("/all", response_model=Iterable[EquipmentReview], status_code=200)
@inject
async def get_all_equipment_reviews(
    service: IEquipmentReviewService = Depends(
        Provide[Container.equipment_review_service]
    ),
) -> Iterable[dict]:
    """An endpoint for getting all equipment reviews.

    Args:
        service (IEquipmentReviewService, optional): The injected equipment review dependency.

    Returns:
        Iterable[dict]: The list of equipment review DTOs.
    """
    review_list = await service.get_all_equipment_reviews()
    return review_list


@router.get("/{equipment_review_id}", response_model=EquipmentReview, status_code=200)
@inject
async def get_equipment_review_by_id(
    equipment_review_id: int,
    service: IEquipmentReviewService = Depends(
        Provide[Container.equipment_review_service]
    ),
) -> dict:
    """An endpoint for getting equipment review by id.

    Args:
        equipment_review_id (int): The equipment review id.
        service (IEquipmentReviewService, optional): The injected equipment review dependency.

    Raises:
        HTTPException: 404 if equipment review does not exist.

    Returns:
        dict: The equipment review DTO.
    """
    if review := await service.get_equipment_review_by_id(equipment_review_id):
        return review

    raise HTTPException(
        status_code=404,
        detail="Equipment review not found",
    )


@router.delete("/{equipment_review_id}", status_code=204)
@inject
async def delete_equipment_review(
    equipment_review_id: int,
    service: IEquipmentReviewService = Depends(
        Provide[Container.equipment_review_service]
    ),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting equipment review.

    Args:
        equipment_review_id (int): The equipment review id.
        service (IEquipmentReviewService, optional): The injected equipment review dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if unauthorized.
        HTTPException: 404 if equipment review does not exist.
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

    if review_data := await service.get_equipment_review_by_id(
        equipment_review_id=equipment_review_id
    ):
        if str(review_data.reviewer_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

    if await service.get_equipment_review_by_id(equipment_review_id):
        await service.delete_equipment_review(equipment_review_id)
        return

    raise HTTPException(
        status_code=404,
        detail="Equipment review not found",
    )


@router.get(
    "/equipment/{equipment_id}",
    response_model=Iterable[EquipmentReview],
    status_code=200,
)
@inject
async def get_reviews_by_equipment_id(
    equipment_id: int,
    service: IEquipmentReviewService = Depends(
        Provide[Container.equipment_review_service]
    ),
) -> Iterable[dict]:
    """An endpoint for getting reviews by equipment id.

    Args:
        equipment_id (int): The equipment id.
        service (IEquipmentReviewService, optional): The injected equipment review dependency.

    Returns:
        Iterable[dict]: The list of equipment review DTOs.
    """
    if reviews := await service.get_reviews_by_equipment_id(equipment_id):
        return reviews
    return []


@router.get(
    "/reviewer/{reviewer_id}", response_model=Iterable[EquipmentReview], status_code=200
)
@inject
async def get_reviews_by_reviewer_id(
    reviewer_id: UUID4,
    service: IEquipmentReviewService = Depends(
        Provide[Container.equipment_review_service]
    ),
) -> Iterable[dict]:
    """An endpoint for getting reviews by reviewer id.

    Args:
        reviewer_id (UUID4): The reviewer UUID4.
        service (IEquipmentReviewService, optional): The injected equipment review dependency.

    Returns:
        Iterable[dict]: The list of equipment review DTOs.
    """
    if reviews := await service.get_reviews_by_reviewer_id(reviewer_id):
        return reviews
    return []


@router.get("/average/{equipment_id}", response_model=float, status_code=200)
@inject
async def get_average_rating_for_equipment(
    equipment_id: int,
    service: IEquipmentReviewService = Depends(
        Provide[Container.equipment_review_service]
    ),
) -> float:
    """An endpoint for getting average rating for equipment.

    Args:
        equipment_id (int): The equipment id.
        service (IEquipmentReviewService, optional): The injected equipment review dependency.

    Returns:
        float: The average rating.
    """
    if rating := await service.get_average_rating_for_equipment(equipment_id):
        return rating
    return 0.0
