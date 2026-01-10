"""Module containing user review database repository implementation."""

from typing import Iterable

from asyncpg import Record  # type: ignore
from pydantic import UUID4
from sqlalchemy import delete, func, insert, select

from src.core.domain.user_review import UserReview, UserReviewIn
from src.core.repositories.iuser_review import IUserReviewRepository
from src.db import database, user_review_table


class UserReviewRepository(IUserReviewRepository):
    """A class implementing the user review repository."""

    async def get_all_user_reviews(self) -> Iterable[UserReview]:
        """The method getting all user reviews from the database.

        Returns:
            Iterable[UserReview]: The collection of all user reviews.
        """
        query = select(user_review_table)
        reviews = await database.fetch_all(query)
        return [UserReview(**dict(review)) for review in reviews]

    async def get_user_review_by_id(self, user_review_id: int) -> UserReview | None:
        """The method getting an user review from the database based on provided id.

        Args:
            user_review_id (int): The id of the user review

        Returns:
            UserReview | None: The user review data if exists.
        """
        review = await self._get_by_id(user_review_id)
        return UserReview(**dict(review)) if review else None

    async def get_sent_reviews_for_user_id(
        self, user_id: UUID4
    ) -> Iterable[UserReview]:
        """The method getting all user reviews sent by provided user id from the database.

        Args:
            user_id (UUID4): The UUID of the user

        Returns:
            Iterable[UserReview] | None: The collection of the all user reviews sent by provided user if exists.
        """
        query = select(user_review_table).where(
            user_review_table.c.reviewer_id == user_id
        )
        reviews = await database.fetch_all(query)
        return [UserReview(**dict(review)) for review in reviews]

    async def get_received_reviews_for_user_id(
        self, user_id: UUID4
    ) -> Iterable[UserReview]:
        """The method getting all user reviews received by provided user id from the database.

        Args:
            user_id (UUID4): The UUID of the user

        Returns:
            Iterable[UserReview] | None: The collection of the all user reviews received by provided user if exists.
        """
        query = select(user_review_table).where(
            user_review_table.c.reviewed_user_id == user_id
        )
        reviews = await database.fetch_all(query)
        return [UserReview(**dict(review)) for review in reviews]

    async def get_average_rating_for_user(self, user_id: UUID4) -> float | None:
        """The method getting average rating for user from the database based on provided user id.

        Args:
            user_id (UUID4): The id of the user

        Returns:
            float | None: The average rating if exists.
        """
        query = select(func.avg(user_review_table.c.rating)).where(
            user_review_table.c.reviewed_user_id == user_id
        )
        result = await database.fetch_val(query)
        return float(result) if result is not None else None

    async def add_user_review(self, data: UserReviewIn) -> UserReview | None:
        """The method adding new user review to the database.

        Args:
            data (UserReviewIn): The attributes of the user review.

        Returns:
            UserReview | None: The newly created user review if exists.
        """
        query = insert(user_review_table).values(data.model_dump())
        new_user_review_id = await database.execute(query)
        new_user_review = await self._get_by_id(new_user_review_id)
        return UserReview(**dict(new_user_review)) if new_user_review else None

    async def delete_user_review(self, user_review_id: int) -> bool:
        """The method removing user review from the database.

        Args:
            user_review_id (int): The id of the user review.

        Returns:
            bool: Success of the operation.
        """
        if await self._get_by_id(user_review_id):
            query = delete(user_review_table).where(
                user_review_table.c.id == user_review_id
            )
            await database.execute(query)
            return True
        return False

    async def _get_by_id(self, user_review_id: int) -> Record | None:
        """The method getting user review from the database based on its ID.

        Args:
            user_review_id (int): The id of the user review.

        Returns:
            Record | None: The user review record if exists.
        """
        query = select(user_review_table).where(
            user_review_table.c.id == user_review_id
        )
        return await database.fetch_one(query)
