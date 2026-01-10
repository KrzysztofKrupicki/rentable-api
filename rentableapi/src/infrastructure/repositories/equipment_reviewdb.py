"""Module containing equipment review database repository implementation."""

from typing import Iterable

from asyncpg import Record  # type: ignore
from pydantic import UUID4
from sqlalchemy import delete, func, insert, select

from src.core.domain.equipment_review import (
    EquipmentReview,
    EquipmentReviewIn,
)
from src.core.repositories.iequipment_review import IEquipmentReviewRepository
from src.db import database, equipment_review_table, equipment_table


class EquipmentReviewRepository(IEquipmentReviewRepository):
    """A class implementing the equipment review repository."""

    async def get_all_equipment_reviews(self) -> Iterable[EquipmentReview]:
        """The method getting all equipment reviews from the database.

        Returns:
            Iterable[EquipmentReview]: The collection of all equipment reviews.
        """
        query = select(equipment_review_table)
        reviews = await database.fetch_all(query)
        return [EquipmentReview(**dict(review)) for review in reviews]

    async def get_equipment_review_by_id(
        self, equipment_review_id: int
    ) -> EquipmentReview | None:
        """The method getting an equipment review from the database based on provided id.

        Args:
            equipment_review_id (int): The id of the equipment review

        Returns:
            EquipmentReview | None: The equipment review data if exists.
        """
        review = await self._get_by_id(equipment_review_id)
        return EquipmentReview(**dict(review)) if review else None

    async def get_reviews_by_equipment_id(
        self, equipment_id: int
    ) -> Iterable[EquipmentReview]:
        """The method getting all equipment reviews from the database based on provided equipment id.

        Args:
            equipment_id (int): The id of the equipment

        Returns:
            Iterable[EquipmentReview] | None: The collection of the all equipment reviews if exists.
        """
        query = select(equipment_review_table).where(
            equipment_review_table.c.equipment_id == equipment_id
        )
        reviews = await database.fetch_all(query)
        return [EquipmentReview(**dict(review)) for review in reviews]

    async def get_reviews_by_reviewer_id(
        self, reviewer_id: UUID4
    ) -> Iterable[EquipmentReview]:
        """The method getting all equipment reviews from the database based on provided reviewer id.

        Args:
            reviewer_id (UUID4): The UUID of the reviewer

        Returns:
            Iterable[EquipmentReview] | None: The collection of the all equipment reviews if exists.
        """
        query = select(equipment_review_table).where(
            equipment_review_table.c.reviewer_id == reviewer_id
        )
        reviews = await database.fetch_all(query)
        return [EquipmentReview(**dict(review)) for review in reviews]

    async def get_average_rating_for_equipment(self, equipment_id: int) -> float | None:
        """The method getting average rating for equipment from the database based on provided equipment id.

        Args:
            equipment_id (int): The id of the equipment

        Returns:
            float | None: The average rating if exists.
        """
        query = select(func.avg(equipment_review_table.c.rating)).where(
            equipment_review_table.c.equipment_id == equipment_id
        )
        result = await database.fetch_val(query)
        return float(result) if result is not None else None

    async def add_equipment_review(
        self, data: EquipmentReviewIn
    ) -> EquipmentReview | None:
        """The method adding new equipment review to the database.

        Args:
            data (EquipmentReviewIn): The attributes of the equipment review.

        Returns:
            EquipmentReview | None: The newly created equipment review if exists.
        """
        query = insert(equipment_review_table).values(**data.model_dump())
        new_equipment_review_id = await database.execute(query)
        new_equipment_review = await self._get_by_id(new_equipment_review_id)
        return (
            EquipmentReview(**dict(new_equipment_review))
            if new_equipment_review
            else None
        )

    async def delete_equipment_review(self, equipment_review_id: int) -> bool:
        """The method removing equipment review from the database.

        Args:
            equipment_review_id (int): The id of the equipment review.

        Returns:
            bool: Success of the operation.
        """
        if await self._get_by_id(equipment_review_id):
            query = delete(equipment_review_table).where(
                equipment_review_table.c.id == equipment_review_id
            )
            await database.execute(query)
            return True
        return False

    async def _get_by_id(self, equipment_review_id: int) -> Record | None:
        """The method getting equipment review from the database based on its ID.

        Args:
            equipment_review_id (int): The id of the equipment review.

        Returns:
            Record | None: The equipment review record if exists.
        """
        query = select(equipment_review_table).where(
            equipment_review_table.c.id == equipment_review_id
        )
        return await database.fetch_one(query)
