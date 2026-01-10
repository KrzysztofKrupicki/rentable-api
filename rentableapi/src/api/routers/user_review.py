"""A module containing user review-related routers."""

from typing import Iterable, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from pydantic import UUID4

from src.container import Container
from src.core.domain.user_review import UserReview, UserReviewIn, UserReviewBroker
from src.infrastructure.services.iuser_review import IUserReviewService
from src.infrastructure.utils import consts

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.post("/create", response_model=UserReview, status_code=201)
@inject
async def create_user_review(
    review: UserReviewIn,
    service: IUserReviewService = Depends(Provide[Container.user_review_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new user review.

    Args:
        review (UserReviewIn): The user review input data.
        service (IUserReviewService, optional): The injected user review dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if unauthorized.

    Returns:
        dict: The created user review attributes.
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

    extended_user_review_data = UserReviewBroker(
        reviewer_id=user_uuid,
        **review.model_dump(),
    )

    if new_user_review := await service.add_user_review(extended_user_review_data):
        return new_user_review.model_dump()


@router.get("/all", response_model=Iterable[UserReview], status_code=200)
@inject
async def get_all_user_reviews(
    service: IUserReviewService = Depends(Provide[Container.user_review_service]),
) -> Iterable[UserReview]:
    """An endpoint for getting all user reviews.

    Args:
        service (IUserReviewService, optional): The injected user review dependency.

    Returns:
        Iterable[UserReview]: The list of user review DTOs.
    """
    return await service.get_all_user_reviews()


@router.get(
    "/user/sent/{user_id}", response_model=Iterable[UserReview], status_code=200
)
@inject
async def get_sent_reviews_for_user_id(
    user_id: UUID4,
    service: IUserReviewService = Depends(Provide[Container.user_review_service]),
) -> Iterable[UserReview]:
    """An endpoint for getting all reviews sent by a user.

    Args:
        user_id (UUID4): The user id.
        service (IUserReviewService, optional): The injected user review dependency.

    Returns:
        Iterable[UserReview]: The list of user review DTOs.
    """
    reviews = await service.get_sent_reviews_for_user_id(user_id)
    return reviews


@router.get(
    "/user/received/{user_id}", response_model=Iterable[UserReview], status_code=200
)
@inject
async def get_received_reviews_for_user_id(
    user_id: UUID4,
    service: IUserReviewService = Depends(Provide[Container.user_review_service]),
) -> Iterable[UserReview]:
    """An endpoint for getting all reviews received by user.

    Args:
        user_id (UUID4): The user id.
        service (IUserReviewService, optional): The injected user review dependency.

    Returns:
        Iterable[UserReview]: The list of user review DTOs.
    """
    reviews = await service.get_received_reviews_for_user_id(user_id)
    return reviews


@router.get("/average/{user_id}", response_model=Optional[float], status_code=200)
@inject
async def get_average_rating_for_user(
    user_id: UUID4,
    service: IUserReviewService = Depends(Provide[Container.user_review_service]),
) -> Optional[float]:
    """An endpoint for getting average rating for a user.

    Args:
        user_id (UUID4): The user id.
        service (IUserReviewService, optional): The injected user review dependency.

    Returns:
        Optional[float]: The average rating.
    """
    return await service.get_average_rating_for_user(user_id)


@router.delete("/{review_id}", status_code=204)
@inject
async def delete_user_review(
    review_id: int,
    service: IUserReviewService = Depends(Provide[Container.user_review_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting user review.

    Args:
        review_id (int): The review id.
        service (IUserReviewService, optional): The injected user review dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if review does not exist.
        HTTPException: 403 if unauthorized.
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

    if review := await service.get_user_review_by_id(review_id):
        if str(review.reviewer_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        await service.delete_user_review(review_id)
        return

    raise HTTPException(
        status_code=404,
        detail="Review not found",
    )
