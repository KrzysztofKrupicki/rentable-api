"""Module containing user review service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from src.core.domain.user_review import UserReview, UserReviewIn


class IUserReviewService(ABC):
    """The abstract class representing protocol of user reviews service."""

    @abstractmethod
    async def get_all_user_reviews(self) -> Iterable[UserReview]:
        """The abstract method getting all user reviews.

        Returns:
            Iterable[UserReview]: User reviews.
        """

    @abstractmethod
    async def get_user_review_by_id(self, user_review_id: int) -> UserReview | None:
        """The abstract method getting user review by provided id.

        Args:
            user_review_id (int): The id of the user review.

        Returns:
            UserReview | None: The user review details.
        """

    @abstractmethod
    async def get_sent_reviews_for_user_id(
        self, user_id: UUID4
    ) -> Iterable[UserReview] | None:
        """The abstract method getting all user reviews sent by provided user id.

        Args:
            user_id (UUID4): The id of the user.

        Returns:
            Iterable[UserReview]: The collection of the all user reviews sent by provided user.
        """

    @abstractmethod
    async def get_received_reviews_for_user_id(
        self, user_id: UUID4
    ) -> Iterable[UserReview] | None:
        """The abstract method getting all user reviews received by provided user id.

        Args:
            user_id (UUID4): The id of the user.

        Returns:
            Iterable[UserReview]: The collection of the all user reviews received by provided user.
        """

    @abstractmethod
    async def get_average_rating_for_user(self, user_id: UUID4) -> float | None:
        """The abstract method getting average rating for the user by provided user id.

        Args:
            user_id (UUID4): The id of the user.

        Returns:
            float | None: The average rating for the user.
        """

    @abstractmethod
    async def add_user_review(self, data: UserReviewIn) -> UserReview | None:
        """The abstract method adding new user review.

        Args:
            data (UserReviewIn): The details of the new user review.

        Returns:
            UserReview | None: The newly created user review.
        """

    @abstractmethod
    async def delete_user_review(self, user_review_id: int) -> bool:
        """The abstract method remmoving user review.

        Args:
            user_review_id (int): The id of the user review.

        Returns:
            bool: Success of the operation.
        """
