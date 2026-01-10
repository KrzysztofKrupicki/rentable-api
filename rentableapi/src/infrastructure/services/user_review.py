"""Module containing user review service implementation."""

from typing import Iterable

from pydantic import UUID4

from src.core.domain.user_review import UserReview, UserReviewIn
from src.core.repositories.iuser_review import IUserReviewRepository
from src.infrastructure.services.iuser_review import IUserReviewService


class UserReviewService(IUserReviewService):
    """A class implementing the user review service."""

    _repository: IUserReviewRepository

    def __init__(self, repository: IUserReviewRepository) -> None:
        """The initializer of the user review service.

        Args:
            repository (IUserReviewRepository): The reference to the repository.
        """
        self._repository = repository

    async def get_user_review_by_id(self, user_review_id: int) -> UserReview | None:
        """The method getting an user review from the repository.

        Args:
            user_review_id (int): The id of the user review.

        Returns:
            UserReview | None: The user review data if exists.
        """
        return await self._repository.get_user_review_by_id(user_review_id)

    async def get_all_user_reviews(self) -> Iterable[UserReview]:
        """The method getting all user reviews from the repository.

        Returns:
            Iterable[UserReview]: The collection of all user reviews.
        """
        return await self._repository.get_all_user_reviews()

    async def get_sent_reviews_for_user_id(
        self, user_id: UUID4
    ) -> Iterable[UserReview]:
        """The method getting all user reviews sent by provided user id from the repository.

        Args:
            user_id (UUID4): The user id.

        Returns:
            Iterable[UserReview]: The collection of all user reviews sent by provided user.
        """
        return await self._repository.get_sent_reviews_for_user_id(user_id)

    async def get_received_reviews_for_user_id(
        self, reviewer_id: UUID4
    ) -> Iterable[UserReview]:
        """The method getting all user reviews received by provided user id from the repository.

        Args:
            reviewer_id (UUID4): The reviewer id.

        Returns:
            Iterable[UserReview]: The collection of all user reviews received by provided user.
        """
        return await self._repository.get_received_reviews_for_user_id(reviewer_id)

    async def get_average_rating_for_user(self, user_id: UUID4) -> float | None:
        """The method getting average rating for user from the repository.

        Args:
            user_id (UUID4): The user id.

        Returns:
            float | None: The average rating for user.
        """
        return await self._repository.get_average_rating_for_user(user_id)

    async def add_user_review(self, data: UserReviewIn) -> UserReview | None:
        """The method adding new user review to the repository.

        Args:
            data (UserReviewIn): The attributes of the user review.

        Returns:
            UserReview | None: The newly created user review.
        """
        return await self._repository.add_user_review(data)

    async def delete_user_review(self, user_review_id: int) -> bool:
        """The method deleting user review from the repository.

        Args:
            user_review_id (int): The user review id.

        Returns:
            bool: The success of the operation.
        """
        return await self._repository.delete_user_review(user_review_id)
